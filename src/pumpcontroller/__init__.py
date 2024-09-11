import sys, os

from PySide6.QtWidgets import QApplication
import qdarktheme
import importlib.metadata
sys.path.append(os.path.dirname(__file__) + "/..")

from pumpcontroller.main import PumpController


__VERSION__ = importlib.metadata.version('PumpController')

def app():
    #QApplication.setStyle("fusion")
    print(f"APP VERSION: {__VERSION__}")
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("light")
    widget = PumpController()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    
    app()
    