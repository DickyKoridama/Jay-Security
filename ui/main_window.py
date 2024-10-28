# ui/main_window.py
from PyQt5 import QtWidgets, uic, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, interface, network_monitor):
        super().__init__()
        uic.loadUi('ui/main_window.ui', self)
        
        self.interface = interface
        self.network_monitor = network_monitor
        
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_network_data)

    def start_update_timer(self):
        self.update_timer.start(100)  # Update setiap 100ms

    def stop_update_timer(self):
        self.update_timer.stop()

    def update_network_data(self):
        while not self.network_monitor.packet_queue.empty():
            packet = self.network_monitor.get_packet()
            if packet:
                self.add_packet_to_table(packet)

    def add_packet_to_table(self, packet):
        row_position = self.networkTable.rowCount()
        self.networkTable.insertRow(row_position)
        self.networkTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(packet["timestamp"]))
        self.networkTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(packet["src_ip"]))
        self.networkTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(packet["dest_ip"]))
        self.networkTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(str(packet["protocol"])))

    def closeEvent(self, event):
        self.stop_update_timer()
        super().closeEvent(event)