# main.py
import sys
import os
from PyQt5 import QtWidgets, QtCore

# Menambahkan direktori proyek ke sys.path
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_dir)

# Mengimpor modul setelah penambahan path
from ui.startup_screen import StartupScreen
from src.interface_selector import InterfaceSelector
from ui.main_window import MainWindow
from ui.logs_window import LogsWindow
from src.log_handler import LogHandler
from src.network_monitor import NetworkMonitor

class MainApp(QtWidgets.QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.interface_selector = None
        self.main_window = None
        self.logs_window = None
        self.network_monitor = None
        self.logger = LogHandler()

        # Tampilkan layar startup terlebih dahulu
        self.startup_screen = StartupScreen()
        self.startup_screen.show()
        self.logger.log_activity("Aplikasi dimulai")

        # Pindah ke InterfaceSelector setelah 3 detik
        QtCore.QTimer.singleShot(3000, self.show_interface_selector)

    def show_interface_selector(self):
        self.startup_screen.close()
        self.interface_selector = InterfaceSelector()
        self.interface_selector.show()
        self.logger.log_activity("Interface Selector dibuka")
        self.interface_selector.selectButton.clicked.connect(self.show_main_window)

    def show_main_window(self):
        selected_interface = self.interface_selector.interfaceComboBox.currentText()
        self.interface_selector.close()

        self.network_monitor = NetworkMonitor(selected_interface)
        self.logger.log_activity(f"Interface '{selected_interface}' dipilih untuk monitoring")

        self.main_window = MainWindow(interface=selected_interface, network_monitor=self.network_monitor)
        self.main_window.show()

        self.main_window.startButton.clicked.connect(self.start_monitoring)
        self.main_window.stopButton.clicked.connect(self.stop_monitoring)
        self.main_window.logButton.clicked.connect(self.show_logs_window)

    def start_monitoring(self):
        if self.network_monitor:
            self.network_monitor.start_monitoring()
            self.main_window.start_update_timer()
            self.logger.log_activity("Pemantauan jaringan dimulai")

    def stop_monitoring(self):
        if self.network_monitor:
            self.network_monitor.stop_monitoring()
            self.main_window.stop_update_timer()
            self.logger.log_activity("Pemantauan jaringan dihentikan")

    def show_logs_window(self):
        if self.logs_window is None:
            self.logs_window = LogsWindow()
        self.logs_window.show()
        self.logger.log_activity("Logs Window dibuka")

    def closeEvent(self, event):
        if self.network_monitor:
            self.network_monitor.stop_monitoring()
        self.logger.log_activity("Aplikasi ditutup")
        self.logger.close_connection()
        super().closeEvent(event)

if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())