# ui/logs_window.py
from PyQt5 import QtWidgets, uic
import sqlite3
from src.config import DATABASE_PATH

class LogsWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/logs_window.ui', self)
        self.load_logs()
        
       
        self.refreshButton.clicked.connect(self.load_logs)
        self.clearButton.clicked.connect(self.clear_logs)

    def load_logs(self):
        """Memuat data serangan dari database dan menampilkannya di tabel."""
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        cursor.execute("SELECT timestamp, attack_type, source_ip, destination_ip, status FROM logs ORDER BY id DESC")
        
        logs = cursor.fetchall()
        self.logsTable.setRowCount(0)

     
        for row_num, row_data in enumerate(logs):
            self.logsTable.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.logsTable.setItem(row_num, col_num, QtWidgets.QTableWidgetItem(str(data)))
        
        connection.close()

    def clear_logs(self):
        """Menghapus semua log serangan dari database dan memperbarui tampilan tabel."""
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM logs")
        connection.commit()
        
        self.logsTable.setRowCount(0)
        
        connection.close()
