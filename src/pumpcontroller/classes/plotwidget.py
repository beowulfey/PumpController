# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Slot

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas


class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(4, 2)))
        self.axes = self.view.figure.subplots()
        self._x = 0
        
        #  Create layout
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.view)
        self.setLayout(vlayout)

        self.data = None
        self.ybot = None
        self.ytop = None
        self.on_change()
        self.run_start = None
#                self.axes.clear()
        self.axes.set_ylabel("Conc (mM)",fontsize="9" )
        self.axes.set_xlabel("Time (min)", fontsize="9")
        plt.rcParams.update({'font.size': 9})
        plt.rcParams["figure.autolayout"] = True
        self.view.figure.tight_layout()
        #print(self.contentsMargins())
        
       

    def set_x(self, currx):
        self._x = currx
        self.on_change()
    
    def set_yax(self, bot, top):
        self.ybot = bot
        self.ytop = top
        self.on_change()
        
    def x(self):
        return self._x
    
    def clear_axes(self):
        self.axes.clear()
        self.axes.set_ylabel("")
        self.axes.set_xlabel("")
        plt.rcParams.update({'font.size': 7})
        self.view.figure.tight_layout()
        #self.view.figure.subplots_adjust(left=0, bottom=0, right=5, top=5, wspace=4, hspace=4)
        #plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    
    def set_start(self, time):
        self.run_start = time
        
    def get_start(self):
        return self.run_start
    
    def set_stop(self):
        self.run_start = None

    @Slot()
    def set_data(self, prot):
        self.data = prot

    def append_data(self, x, y):
        self.data.xvals().append(x)
        self.data.yvals().append(y)
        self.on_change()
    
    @Slot()
    def on_change(self, data=None):
        """ Update the plot with the current input values """

        if data is not None:
            self.set_data(data)
        
        
        if self.data is not None:
            x = self.data.xvals()
            y = self.data.yvals()
        else:
            x = []
            y = []

        self.axes.clear()
        self.axes.plot(x, y, color='#DE655E')
        
        if self._x > 0:
            self.axes.axvline(self._x, color='#75B9D7')
        if self.ybot:
            self.axes.set_ylabel("Conc (mM)",fontsize="9" )
            self.axes.set_xlabel("Time (min)", fontsize="9")
            self.axes.set_ylim(self.ybot, self.ytop)
        self.view.draw()
