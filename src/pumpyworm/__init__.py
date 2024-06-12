import sys

from PySide6.QtWidgets import QApplication


from pumpyworm.main import PumPyWorm


__VERSION__ = "1.0.1"

def app():
    QApplication.setStyle("fusion")
    app = QApplication(sys.argv)
    widget = PumPyWorm()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    app()
    