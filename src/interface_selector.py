# src/interface_selector.py
import psutil
from PyQt5 import QtWidgets, uic

class InterfaceSelector(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Memuat file UI untuk Interface Selector
        uic.loadUi('ui/interface_selector.ui', self)

        # Mengisi QComboBox dengan daftar interface jaringan yang tersedia
        self.populate_interfaces()

        # Menghubungkan tombol konfirmasi untuk memilih interface
        self.selectButton.clicked.connect(self.confirm_selection)

    def populate_interfaces(self):
        """Mengisi ComboBox dengan daftar interface jaringan."""
        interfaces = psutil.net_if_addrs().keys()  # Mendapatkan nama-nama interface jaringan
        self.interfaceComboBox.addItems(interfaces)  # Isi QComboBox dengan interface

    def confirm_selection(self):
        """Konfirmasi pemilihan interface dan lanjutkan proses."""
        selected_interface = self.interfaceComboBox.currentText()
        print(f"Interface yang dipilih: {selected_interface}")
        # Lanjutkan logika lainnya di sini (misalnya, monitoring jaringan)
        self.close()
