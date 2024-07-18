# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QAbstractSpinBox, QApplication,
    QComboBox, QDoubleSpinBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStatusBar, QTableView, QTextEdit,
    QVBoxLayout, QWidget)

from plotwidget import PlotWidget

class Ui_PumPyWorm(object):
    def setupUi(self, PumPyWorm):
        if not PumPyWorm.objectName():
            PumPyWorm.setObjectName(u"PumPyWorm")
        PumPyWorm.resize(926, 651)
        self.actionQuit = QAction(PumPyWorm)
        self.actionQuit.setObjectName(u"actionQuit")
        self.centralwidget = QWidget(PumPyWorm)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.centralwidget.setFont(font)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_5, 0, 1, 1, 1)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.combo_com = QComboBox(self.frame_4)
        self.combo_com.setObjectName(u"combo_com")

        self.gridLayout_2.addWidget(self.combo_com, 2, 1, 1, 1)

        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 6, 0, 1, 1)

        self.spin_pac = QSpinBox(self.frame_4)
        self.spin_pac.setObjectName(u"spin_pac")
        self.spin_pac.setMaximum(200)

        self.gridLayout_2.addWidget(self.spin_pac, 5, 1, 1, 1)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        font1 = QFont()
        font1.setFamilies([u".AppleSystemUIFont"])
        font1.setBold(True)
        self.label_7.setFont(font1)

        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 2)

        self.spin_pbc = QSpinBox(self.frame_4)
        self.spin_pbc.setObjectName(u"spin_pbc")
        self.spin_pbc.setMaximum(200)

        self.gridLayout_2.addWidget(self.spin_pbc, 6, 1, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)

        self.but_confirm_settings = QPushButton(self.frame_4)
        self.but_confirm_settings.setObjectName(u"but_confirm_settings")

        self.gridLayout_2.addWidget(self.but_confirm_settings, 7, 1, 1, 1)

        self.spin_flow_rate = QDoubleSpinBox(self.frame_4)
        self.spin_flow_rate.setObjectName(u"spin_flow_rate")

        self.gridLayout_2.addWidget(self.spin_flow_rate, 4, 1, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 3, 0, 1, 1)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 4, 0, 1, 1)

        self.spin_refresh = QDoubleSpinBox(self.frame_4)
        self.spin_refresh.setObjectName(u"spin_refresh")
        self.spin_refresh.setDecimals(1)
        self.spin_refresh.setMinimum(0.100000000000000)
        self.spin_refresh.setMaximum(1.000000000000000)
        self.spin_refresh.setSingleStep(0.100000000000000)
        self.spin_refresh.setStepType(QAbstractSpinBox.DefaultStepType)
        self.spin_refresh.setValue(0.500000000000000)

        self.gridLayout_2.addWidget(self.spin_refresh, 3, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)


        self.verticalLayout_5.addWidget(self.frame_4)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.spin_straight_conc = QSpinBox(self.frame)
        self.spin_straight_conc.setObjectName(u"spin_straight_conc")

        self.gridLayout_3.addWidget(self.spin_straight_conc, 2, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.but_start_pump = QPushButton(self.frame)
        self.but_start_pump.setObjectName(u"but_start_pump")

        self.horizontalLayout.addWidget(self.but_start_pump)

        self.but_update_pump = QPushButton(self.frame)
        self.but_update_pump.setObjectName(u"but_update_pump")

        self.horizontalLayout.addWidget(self.but_update_pump)

        self.but_stop_pump = QPushButton(self.frame)
        self.but_stop_pump.setObjectName(u"but_stop_pump")

        self.horizontalLayout.addWidget(self.but_stop_pump)


        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 0, 1, 2)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)

        self.label_11 = QLabel(self.frame)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout_3)


        self.verticalLayout_5.addWidget(self.frame)


        self.gridLayout_5.addLayout(self.verticalLayout_5, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_7, 3, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.frame_3 = QFrame(self.centralwidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_15 = QLabel(self.frame_3)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_4.addWidget(self.label_15, 3, 0, 1, 1)

        self.spin_start_conc = QSpinBox(self.frame_3)
        self.spin_start_conc.setObjectName(u"spin_start_conc")
        self.spin_start_conc.setSingleStep(10)

        self.gridLayout_4.addWidget(self.spin_start_conc, 4, 1, 1, 1)

        self.spin_seg_time = QDoubleSpinBox(self.frame_3)
        self.spin_seg_time.setObjectName(u"spin_seg_time")
        self.spin_seg_time.setMaximum(2.000000000000000)
        self.spin_seg_time.setSingleStep(0.050000000000000)
        self.spin_seg_time.setStepType(QAbstractSpinBox.DefaultStepType)

        self.gridLayout_4.addWidget(self.spin_seg_time, 3, 1, 1, 1)

        self.line = QFrame(self.frame_3)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line, 1, 0, 1, 2)

        self.label_17 = QLabel(self.frame_3)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_4.addWidget(self.label_17, 4, 0, 1, 1)

        self.label_16 = QLabel(self.frame_3)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_4.addWidget(self.label_16, 5, 0, 1, 1)

        self.but_clear_segments = QPushButton(self.frame_3)
        self.but_clear_segments.setObjectName(u"but_clear_segments")

        self.gridLayout_4.addWidget(self.but_clear_segments, 6, 1, 1, 1)

        self.but_add_segment = QPushButton(self.frame_3)
        self.but_add_segment.setObjectName(u"but_add_segment")

        self.gridLayout_4.addWidget(self.but_add_segment, 6, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.label_18 = QLabel(self.frame_3)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font1)

        self.gridLayout_4.addWidget(self.label_18, 2, 0, 1, 2)

        self.spin_end_conc = QSpinBox(self.frame_3)
        self.spin_end_conc.setObjectName(u"spin_end_conc")
        self.spin_end_conc.setSingleStep(10)

        self.gridLayout_4.addWidget(self.spin_end_conc, 5, 1, 1, 1)

        self.line_2 = QFrame(self.frame_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_4.addWidget(self.line_2, 7, 0, 1, 2)


        self.horizontalLayout_4.addLayout(self.gridLayout_4)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_19 = QLabel(self.frame_3)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font1)

        self.verticalLayout_7.addWidget(self.label_19)

        self.table_segments = QTableView(self.frame_3)
        self.table_segments.setObjectName(u"table_segments")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_segments.sizePolicy().hasHeightForWidth())
        self.table_segments.setSizePolicy(sizePolicy)
        self.table_segments.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.table_segments.setDragEnabled(True)
        self.table_segments.setDragDropMode(QAbstractItemView.DragDrop)
        self.table_segments.setAlternatingRowColors(True)
        self.table_segments.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table_segments.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_7.addWidget(self.table_segments)

        self.verticalLayout_7.setStretch(1, 1)

        self.horizontalLayout_4.addLayout(self.verticalLayout_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.label_20 = QLabel(self.frame_3)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_20)

        self.widget_plots = PlotWidget(self.frame_3)
        self.widget_plots.setObjectName(u"widget_plots")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_plots.sizePolicy().hasHeightForWidth())
        self.widget_plots.setSizePolicy(sizePolicy1)
        self.widget_plots.setMinimumSize(QSize(100, 200))

        self.verticalLayout_2.addWidget(self.widget_plots)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.but_start_protocol = QPushButton(self.frame_3)
        self.but_start_protocol.setObjectName(u"but_start_protocol")

        self.horizontalLayout_3.addWidget(self.but_start_protocol)

        self.but_update_protocol = QPushButton(self.frame_3)
        self.but_update_protocol.setObjectName(u"but_update_protocol")

        self.horizontalLayout_3.addWidget(self.but_update_protocol)

        self.but_stop_protocol = QPushButton(self.frame_3)
        self.but_stop_protocol.setObjectName(u"but_stop_protocol")

        self.horizontalLayout_3.addWidget(self.but_stop_protocol)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.gridLayout.addWidget(self.frame_3, 1, 2, 1, 1)

        self.console = QTextEdit(self.centralwidget)
        self.console.setObjectName(u"console")
        self.console.setAcceptDrops(False)
        self.console.setUndoRedoEnabled(False)
        self.console.setReadOnly(True)

        self.gridLayout.addWidget(self.console, 2, 1, 1, 2)

        PumPyWorm.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(PumPyWorm)
        self.statusBar.setObjectName(u"statusBar")
        PumPyWorm.setStatusBar(self.statusBar)
        QWidget.setTabOrder(self.combo_com, self.spin_flow_rate)
        QWidget.setTabOrder(self.spin_flow_rate, self.spin_pac)
        QWidget.setTabOrder(self.spin_pac, self.spin_pbc)
        QWidget.setTabOrder(self.spin_pbc, self.but_confirm_settings)
        QWidget.setTabOrder(self.but_confirm_settings, self.spin_straight_conc)
        QWidget.setTabOrder(self.spin_straight_conc, self.but_start_pump)
        QWidget.setTabOrder(self.but_start_pump, self.but_update_pump)
        QWidget.setTabOrder(self.but_update_pump, self.but_stop_pump)
        QWidget.setTabOrder(self.but_stop_pump, self.spin_seg_time)
        QWidget.setTabOrder(self.spin_seg_time, self.spin_start_conc)
        QWidget.setTabOrder(self.spin_start_conc, self.spin_end_conc)
        QWidget.setTabOrder(self.spin_end_conc, self.but_add_segment)
        QWidget.setTabOrder(self.but_add_segment, self.but_clear_segments)
        QWidget.setTabOrder(self.but_clear_segments, self.table_segments)
        QWidget.setTabOrder(self.table_segments, self.but_start_protocol)
        QWidget.setTabOrder(self.but_start_protocol, self.but_stop_protocol)

        self.retranslateUi(PumPyWorm)

        QMetaObject.connectSlotsByName(PumPyWorm)
    # setupUi

    def retranslateUi(self, PumPyWorm):
        PumPyWorm.setWindowTitle(QCoreApplication.translate("PumPyWorm", u"AWpumps", None))
        self.actionQuit.setText(QCoreApplication.translate("PumPyWorm", u"Quit", None))
        self.label_6.setText(QCoreApplication.translate("PumPyWorm", u"Pump B Syringe Conc (mM)", None))
        self.label_7.setText(QCoreApplication.translate("PumPyWorm", u"Pump Settings", None))
        self.label_5.setText(QCoreApplication.translate("PumPyWorm", u"Pump A Syringe Conc (mM)", None))
        self.but_confirm_settings.setText(QCoreApplication.translate("PumPyWorm", u"Confirm", None))
        self.label_2.setText(QCoreApplication.translate("PumPyWorm", u"Refresh Rate (sec)", None))
        self.label.setText(QCoreApplication.translate("PumPyWorm", u"COM Port:", None))
        self.label_4.setText(QCoreApplication.translate("PumPyWorm", u"Flow Rate (ml/min)", None))
        self.but_start_pump.setText(QCoreApplication.translate("PumPyWorm", u"Start", None))
        self.but_update_pump.setText(QCoreApplication.translate("PumPyWorm", u"Update", None))
        self.but_stop_pump.setText(QCoreApplication.translate("PumPyWorm", u"Stop", None))
        self.label_10.setText(QCoreApplication.translate("PumPyWorm", u"Concentration", None))
        self.label_11.setText(QCoreApplication.translate("PumPyWorm", u"Straight Run", None))
        self.label_15.setText(QCoreApplication.translate("PumPyWorm", u"Time (min)", None))
        self.label_17.setText(QCoreApplication.translate("PumPyWorm", u"Start Conc (mM)", None))
        self.label_16.setText(QCoreApplication.translate("PumPyWorm", u"End Conc (mM)", None))
        self.but_clear_segments.setText(QCoreApplication.translate("PumPyWorm", u"Clear All", None))
        self.but_add_segment.setText(QCoreApplication.translate("PumPyWorm", u"Add Segment", None))
        self.label_18.setText(QCoreApplication.translate("PumPyWorm", u"Add Segment", None))
        self.label_19.setText(QCoreApplication.translate("PumPyWorm", u"Current Segments", None))
        self.label_20.setText(QCoreApplication.translate("PumPyWorm", u"Current protocol", None))
        self.but_start_protocol.setText(QCoreApplication.translate("PumPyWorm", u"Start", None))
        self.but_update_protocol.setText(QCoreApplication.translate("PumPyWorm", u"Update", None))
        self.but_stop_protocol.setText(QCoreApplication.translate("PumPyWorm", u"Stop", None))
    # retranslateUi

