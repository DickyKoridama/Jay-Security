# main.py/dicky
import sys
import os
from PyQt5 import QtWidgets, QtCore
from src.network_monitor import NetworkMonitor
from src.log_handler import LogHandler
from ui.startup_screen import StartupScreen
from src.interface_selector import InterfaceSelector
from ui.main_window import MainWindow
from ui.logs_window import LogsWindow
from src.utils.fsa_utils import initialize_fsa  
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class MainApp(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.interface_selector = None
        self.main_window = None
        self.logs_window = None
        self.network_monitor = None
        self.logger = LogHandler()

        # Show startup screen
        self.startup_screen = StartupScreen()
        self.startup_screen.show()

       
        QtCore.QTimer.singleShot(3000, self.show_interface_selector)

    def show_interface_selector(self):
        """Show the interface selector window."""
        try:
            self.startup_screen.close()
            self.interface_selector = InterfaceSelector()
            self.interface_selector.show()
            self.interface_selector.selectButton.clicked.connect(self.show_main_window)
        except Exception as e:
            self.logger.log_activity(f"Error showing interface selector: {e}", level="error")

    def show_main_window(self):
        """Show the main window after selecting an interface."""
        try:
            selected_interface = self.interface_selector.interfaceComboBox.currentText()
            if not selected_interface:
                raise ValueError("No network interface selected!")

            self.interface_selector.close()

           
            fsa_detector = initialize_fsa()  
            self.network_monitor = NetworkMonitor(
                interface=selected_interface,
                fsa_detector=fsa_detector
            )

            self.main_window = MainWindow(interface=selected_interface, network_monitor=self.network_monitor)
            self.main_window.show()

            
            self.main_window.startButton.clicked.connect(self.start_monitoring)
            self.main_window.stopButton.clicked.connect(self.stop_monitoring)
            self.main_window.logButton.clicked.connect(self.show_logs_window)
        except Exception as e:
            self.logger.log_activity(f"Error initializing main window: {e}", level="error")

    def start_monitoring(self):
        """Start network monitoring."""
        try:
            if self.network_monitor:
                self.network_monitor.start_monitoring()
                self.main_window.start_update_timer()
                self.logger.log_activity("Started network monitoring", level="info")
        except Exception as e:
            self.logger.log_activity(f"Error starting monitoring: {e}", level="error")

    def stop_monitoring(self):
        """Stop network monitoring."""
        try:
            if self.network_monitor:
                self.network_monitor.stop_monitoring()
                self.main_window.stop_update_timer()
                self.logger.log_activity("Stopped network monitoring", level="info")
        except Exception as e:
            self.logger.log_activity(f"Error stopping monitoring: {e}", level="error")

    def show_logs_window(self):
        """Show the logs window."""
        try:
            if self.logs_window is None:
                self.logs_window = LogsWindow()
            self.logs_window.show()
        except Exception as e:
            self.logger.log_activity(f"Error showing logs window: {e}", level="error")

    def closeEvent(self, event):
        """Handle application exit."""
        try:
            if self.network_monitor:
                self.network_monitor.stop_monitoring()
            self.logger.log_activity("Application closed", level="info")
            self.logger.close()
            super().closeEvent(event)
        except Exception as e:
            self.logger.log_activity(f"Error during application close: {e}", level="error")
            super().closeEvent(event)


if __name__ == "__main__":
    try:
        app = MainApp(sys.argv)
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Critical error: {e}")
