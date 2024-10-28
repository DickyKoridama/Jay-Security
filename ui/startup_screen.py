# ui/startup_screen.py
from PyQt5 import QtWidgets, uic, QtGui

class StartupScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Memuat file UI untuk Startup Screen
        uic.loadUi('ui/startup_screen.ui', self)

        # Memuat logo ke dalam QLabel "Logo"
        self.logo_pixmap = QtGui.QPixmap("assets/icons/tes3.png")  # Path ke logo
        self.Logo.setPixmap(self.logo_pixmap)
        self.Logo.setScaledContents(True)  # Agar gambar menyesuaikan dengan QLabel

        # Memuat GIF spinner ke dalam QLabel "spinnerLabel"
        self.spinner_movie = QtGui.QMovie("assets/icons/spinner2.gif")  # Path ke GIF spinner
        self.spinnerLabel.setMovie(self.spinner_movie)
        self.spinner_movie.start()  # Mulai animasi GIF
