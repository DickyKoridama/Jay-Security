# src/interface_selector.py
import psutil
from PyQt5 import QtWidgets, uic

class InterfaceSelector(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
       
        uic.loadUi('ui/interface_selector.ui', self)

    
        self.populate_interfaces()

        
        self.selectButton.clicked.connect(self.confirm_selection)

    def populate_interfaces(self):
        """Mengisi ComboBox dengan daftar interface jaringan."""
        interfaces = psutil.net_if_addrs().keys() 
        self.interfaceComboBox.addItems(interfaces)  

    def confirm_selection(self):
        """Konfirmasi pemilihan interface dan lanjutkan proses."""
        selected_interface = self.interfaceComboBox.currentText()
        print(f"Interface yang dipilih: {selected_interface}")
       
        self.close()
