import sys

from PySide6.QtWidgets import QApplication
import qdarktheme

from pumpcontroller.main import PumpController


__VERSION__ = "1.2.0"

def app():
    #QApplication.setStyle("fusion")
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    widget = PumpController()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app()
    