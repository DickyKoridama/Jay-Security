from PyQt5 import QtWidgets, uic, QtGui, QtCore
import sys

class StartupScreen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/startup_screen.ui', self)
        
        # Center the window on the screen
        self.center()

        # Load logo and spinner (as shown in previous example)
        self.logo_pixmap = QtGui.QPixmap("assets/icons/tes3.png")
        self.Logo.setPixmap(self.logo_pixmap)
        self.Logo.setScaledContents(True)

        self.spinner_movie = QtGui.QMovie("assets/icons/spinner2.gif")
        self.spinnerLabel.setMovie(self.spinner_movie)
        self.spinner_movie.start()

        # Fade-in effect
        self.setWindowOpacity(0)
        self.fade_in_effect = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_in_effect.setDuration(1000)
        self.fade_in_effect.setStartValue(0)
        self.fade_in_effect.setEndValue(1)
        self.fade_in_effect.start()

        self.show()

    def center(self):
        """Center the window on the screen."""
        qr = self.frameGeometry()  # Get the window's geometry
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()  # Get the center of the screen
        qr.moveCenter(cp)  # Move the window's geometry to the center
        self.move(qr.topLeft())  # Move the window to the top-left of the geometry

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = StartupScreen()
    sys.exit(app.exec_())