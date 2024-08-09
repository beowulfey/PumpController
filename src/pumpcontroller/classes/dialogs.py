from serial.tools import list_ports

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Signal

from pumpcontroller.ui.ui_ports import Ui_Dialog

class COM_dialog(Ui_Dialog, QDialog):
    
    coms = Signal(str, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        # Run the .setupUi() method to show the GUI
        self.setupUi(self)
        
        self.combo_com_pump.addItem("None")
        self.combo_com_cond.addItem("None")
        self.combo_com_pump.addItem("TEST")
        self.combo_com_cond.addItem("TEST")
        self.combo_com_pump.addItems([str(_port).split(" ")[0] for _port in list_ports.comports()])
        self.combo_com_cond.addItems([str(_port).split(" ")[0] for _port in list_ports.comports()])
        self.combo_com_cond.currentIndexChanged.connect(self.update_pump)
        self.combo_com_pump.currentIndexChanged.connect(self.update_cond)
        
    def update_cond(self):
        if self.combo_com_pump.currentIndex() == self.combo_com_cond.currentIndex() > 0: 
            self.combo_com_cond.setCurrentIndex(self.combo_com_cond.currentIndex()-1)
            
    
    def update_pump(self):
        if self.combo_com_pump.currentIndex() == self.combo_com_cond.currentIndex() > 0: 
            self.combo_com_pump.setCurrentIndex(self.combo_com_pump.currentIndex()-1)
           
    def accept(self):
        #if self.combo_com_cond.currentIndex() != 0 and self.combo_com_pump.currentIndex() != 0:
        #    print("SET 1")
        self.coms.emit(self.combo_com_cond.currentText(), self.combo_com_pump.currentText())
        #elif self.combo_com_cond.currentIndex() != 0 and self.combo_com_pump.currentIndex() == 0:
        #    print("SET 2")
        #    self.coms.emit(self.combo_com_cond.currentText(), None)
        #elif self.combo_com_cond.currentIndex() == 0 and self.combo_com_pump.currentIndex() != 0:
        #    print("SET 3")
        #    self.coms.emit(None, self.combo_com_pump.currentText())
        #else:
        #    print("SET 4")
        #    self.coms.emit(None, None)
        super().accept()
                       
        
    