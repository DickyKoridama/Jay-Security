# main_window.py
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, interface, network_monitor):
        super().__init__()
        uic.loadUi('ui/main_window.ui', self)
        
        self.interface = interface
        self.network_monitor = network_monitor
        
        # Timer untuk memperbarui data jaringan setiap 1 detik
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_network_data)

        # Menghubungkan tombol dengan fungsi monitoring
        self.startButton.clicked.connect(self.start_monitoring)
        self.stopButton.clicked.connect(self.stop_monitoring)

    def start_monitoring(self):
        """Mulai monitoring jaringan dan timer update data."""
        self.network_monitor.start_monitoring()
        self.statusLabel.setText("Status: Sedang Memantau")
        self.start_update_timer()

    def stop_monitoring(self):
        """Hentikan monitoring jaringan dan timer update data."""
        self.network_monitor.stop_monitoring()
        self.statusLabel.setText("Status: Menunggu")
        self.stop_update_timer()

    def start_update_timer(self):
        """Mulai timer untuk memperbarui data jaringan di GUI."""
        self.update_timer.start(1000)  # Update setiap 1 detik

    def stop_update_timer(self):
        """Hentikan timer pembaruan."""
        self.update_timer.stop()

    def update_network_data(self):
        """Ambil data dari antrian dan tampilkan di GUI."""
        while not self.network_monitor.packet_queue.empty():
            packet = self.network_monitor.get_packet()
            if packet:
                # Tampilkan peringatan jika serangan terdeteksi
                if "alert" in packet:
                    alert_msg = f"⚠️ Serangan terdeteksi: {packet['alert']} dari {packet['src_ip']}"
                    self.statusLabel.setText(alert_msg)
                    self.show_popup_notification(alert_msg)
                else:
                    # Tambahkan data paket ke tabel tampilan
                    self.add_packet_to_table(packet)

    def add_packet_to_table(self, packet):
        """Menambahkan data paket ke tabel."""
        row_position = self.networkTable.rowCount()
        self.networkTable.insertRow(row_position)
        self.networkTable.setItem(row_position, 0, QtWidgets.QTableWidgetItem(packet["src_ip"]))
        self.networkTable.setItem(row_position, 1, QtWidgets.QTableWidgetItem(packet["dest_ip"]))
        self.networkTable.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(packet["protocol"])))
        self.networkTable.setItem(row_position, 3, QtWidgets.QTableWidgetItem(packet["timestamp"]))
        self.networkTable.setItem(row_position, 4, QtWidgets.QTableWidgetItem(packet.get("info", "")))

    def show_popup_notification(self, message):
        """Menampilkan popup notifikasi di desktop."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Notifikasi Keamanan")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.show()

    def closeEvent(self, event):
        """Hentikan pembaruan data ketika jendela ditutup."""
        self.stop_update_timer()
        super().closeEvent(event)
