
from PySide6.QtCore import QThread, Slot, Signal
     
class Worker(QThread):
    result = Signal(tuple)
    def __init__(self, target):#, slotOnFinished = None):
        super(Worker, self).__init__()
        self.target = target
        #if slotOnFinished:
        #    self.result.connect(slotOnFinished)

    def run(self, *args, **kwargs):
        result = None
        while not result:
            result = self.target(*args, **kwargs)
        self.result.emit(result)