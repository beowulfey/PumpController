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
        #self.toolbar = NavigationToolbar2QT(self.view, self)

        
        #  Create layout
        vlayout = QVBoxLayout()
        #vlayout.addWidget(self.toolbar)
        vlayout.addWidget(self.view)
        self.setLayout(vlayout)

        # connect inputs with on_change method
        #self.mu_input.valueChanged.connect(self.on_change)
        #self.std_input.valueChanged.connect(self.on_change)
        self.protocol = None
        self.ybot = 0
        self.ytop = 100
        self.on_change()
       

    def set_x(self, currx):
        self._x = currx
        self.on_change()
    
    def set_yax(self, bot, top):
        self.ybot = bot
        self.ytop = top
        self.on_change()
        
    def x(self):
        return self._x

    @Slot()
    def set_protocol(self, prot):
        self.protocol = prot

    @Slot()
    def on_change(self, protocol=None):
        """ Update the plot with the current input values """

        if protocol is not None:
            self.set_protocol(protocol)
        
        
        if self.protocol is not None:
            x = self.protocol.xvals()
            y = self.protocol.yvals()
        else:
            x = []
            y = []
        self.axes.clear()
        self.axes.set_ylabel("Conc (mM)",fontsize="9" )
        self.axes.set_xlabel("Time (min)", fontsize="9")
        plt.rcParams.update({'font.size': 9})
        self.view.figure.tight_layout()
        self.axes.plot(x, y, color='#DE655E')
        if self._x > 0:
            self.axes.axvline(self._x, color='#75B9D7')
        self.axes.set_ylim(self.ybot, self.ytop)
        self.view.draw()
