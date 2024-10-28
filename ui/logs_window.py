# ui/logs_window.py
from PyQt5 import QtWidgets, uic

class LogsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Memuat file .ui untuk Logs Window
        uic.loadUi('ui/logs_window.ui', self)

        # Menghubungkan tombol Refresh dan Clear
        self.refreshButton.clicked.connect(self.refresh_log)
        self.clearButton.clicked.connect(self.clear_log)

    def refresh_log(self):
        """Fungsi untuk menyegarkan log di tabel."""
        # Contoh data log (untuk pengujian)
        data = [
            ("2024-10-15 14:32", "DDoS", "192.168.1.100", "8.8.8.8", "Mitigated"),
            ("2024-10-15 14:40", "Port Scan", "192.168.1.101", "8.8.4.4", "Unmitigated"),
            ("2024-10-15 15:02", "Malware", "192.168.1.102", "8.8.8.8", "Mitigated"),
        ]

        # Menghapus data lama di tabel
        self.logsTable.setRowCount(0)

        # Memasukkan data log ke dalam tabel
        for row, (time, attack_type, src_ip, dest_ip, status) in enumerate(data):
            self.logsTable.insertRow(row)
            self.logsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(time))
            self.logsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(attack_type))
            self.logsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(src_ip))
            self.logsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(dest_ip))
            self.logsTable.setItem(row, 4, QtWidgets.QTableWidgetItem(status))

    def clear_log(self):
        """Fungsi untuk menghapus semua data log dari tabel."""
        self.logsTable.setRowCount(0)
