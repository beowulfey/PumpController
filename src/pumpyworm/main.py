# This Python file uses the following encoding: utf-8
from datetime import datetime
from serial.tools import list_ports

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QHeaderView
from PySide6.QtGui import QAction, QColor, QTextCursor, QColorConstants

    

from pumpyworm.external import nesp_lib
from pumpyworm.classes.tablemodel import TableModel
from pumpyworm.classes.protocol import Protocol
from pumpyworm.ui.ui_form import Ui_PumPyWorm
from pumpyworm.constants import FMT, RED, GREEN

# Important:
# Run the following command to generate the ui_form.py file in the UI directory
#     pyside6-uic form.ui -o ui_form.py


# TO DO
# ADD UPDATE PROTOCOL BUTTON
# CAN'T SEND PROTOCOL WHILE PUMP IS RUNNING!! 


class PumPyWorm(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_PumPyWorm()
        self.ui.setupUi(self)
        self.setWindowTitle('PumPy Worm')
        #self.ui.console.setTextInteractionFlags(TextSelectableByKeyboard | TextSelectableByMouse)

        ## INITIATE PUMP SETTINGS
        self.ui.combo_com.addItem("None")
        self.ui.combo_com.addItems([str(_port).split(" ")[0] for _port in list_ports.comports()])
        self.ui.spin_flow_rate.setValue(0.4)
        self.ui.spin_pac.setValue(0)
        self.ui.spin_pbc.setValue(100)
        self.ui.but_confirm_settings.setMinimumWidth(93)
        
        
        self.port = None
        self.pumps = None

        model = TableModel()
    
        self.ui.table_segments.setModel(model)
        #self.ui.table.horizontalHeader().setCascadingSectionResizes(True)
        self.ui.table_segments.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.phases = []
        
        self.protocol = Protocol()
        
        
        self.run_timer = QTimer()
        self.run_timer.setSingleShot(True)
        
        self.int_timer = QTimer()
        self.int_timer.setSingleShot(True)
        
        offset = max(self.ui.spin_pac.value(), self.ui.spin_pbc.value()) * 0.10
        self.ui.widget_plots.set_yax(min(self.ui.spin_pac.value(), self.ui.spin_pbc.value())-offset,max(self.ui.spin_pac.value(), self.ui.spin_pbc.value())+offset)
        
        


        ## DISABLE EVERYTHING BEFORE PUMP CONFIRMATION
        self.ui.spin_straight_conc.setDisabled(True)
        self.ui.but_start_pump.setDisabled(True)
        self.ui.but_update_pump.setDisabled(True)
        self.ui.but_stop_pump.setDisabled(True)
        self.ui.spin_seg_time.setDisabled(True)
        self.ui.spin_start_conc.setDisabled(True)
        self.ui.spin_end_conc.setDisabled(True)
        self.ui.but_add_segment.setDisabled(True)
        self.ui.but_clear_segments.setDisabled(True)
        self.ui.table_segments.setDisabled(True)
        self.ui.but_start_protocol.setDisabled(True)
        self.ui.but_stop_protocol.setDisabled(True)


        # Create exit action with icon, shortcut, status tip and close window click event
        act_exit = QAction('&Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        act_exit.triggered.connect(self.close)
        act_save_log = QAction('&Save Log', self)
        act_save_log.setShortcut('Ctrl+Shift+S')
        act_save_log.setStatusTip('Save log file')
        act_save_log.triggered.connect(self.save_log)
        act_reset_pumps = QAction('&Reset Pumps', self)
        act_reset_pumps.triggered.connect(self.reset_pumps)

        # Create menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        # Add File menu
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(act_exit)
        menu_file.addAction(act_save_log)
        #menu_file.addAction(act_reset_pumps)


        # Link signals to slots
        self.ui.combo_com.currentIndexChanged.connect(self.settings_changed)
        self.ui.spin_flow_rate.valueChanged.connect(self.settings_changed)
        self.ui.spin_pac.valueChanged.connect(self.settings_changed)
        self.ui.spin_pbc.valueChanged.connect(self.settings_changed)
        self.ui.but_confirm_settings.clicked.connect(self.confirm_settings)
        self.ui.but_start_pump.clicked.connect(self.start_pump)
        self.ui.but_stop_pump.clicked.connect(self.stop_pump)
        self.ui.but_update_pump.clicked.connect(self.update_pump)
        self.ui.but_add_segment.clicked.connect(self.add_segment)
        self.ui.but_clear_segments.clicked.connect(self.clear_segments)
        self.ui.but_start_protocol.clicked.connect(self.start_protocol)
        self.ui.but_stop_protocol.clicked.connect(self.stop_protocol)
        self.int_timer.timeout.connect(self.timer_tick)
        
        self.ui.table_segments.resizeColumnsToContents()
        #self.ui.spin_straight_conc.valueChanged.connect(self.enable_update)


    ## SLOTS

    def settings_changed(self):
        self.ui.but_confirm_settings.setEnabled(True)
        self.ui.but_confirm_settings.setStyleSheet('QPushButton { color: black;}')
        self.ui.but_confirm_settings.setText("Confirm")
        self.ui.spin_straight_conc.setDisabled(True)
        self.ui.but_start_pump.setDisabled(True)
        self.ui.but_update_pump.setDisabled(True)
        self.ui.but_stop_pump.setDisabled(True)
        self.ui.spin_seg_time.setDisabled(True)
        self.ui.spin_start_conc.setDisabled(True)
        self.ui.spin_end_conc.setDisabled(True)
        self.ui.but_add_segment.setDisabled(True)
        self.ui.but_clear_segments.setDisabled(True)
        self.ui.table_segments.setDisabled(True)
        self.ui.but_start_protocol.setDisabled(True)
        self.ui.but_stop_protocol.setDisabled(True)

    def confirm_settings(self):
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} PUMP SETTINGS CONFIRMED:", color=GREEN)
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Refresh rate: {self.ui.spin_refresh.value()}; Flow Rate: {self.ui.spin_flow_rate.value()}; PAC: {self.ui.spin_pac.value()}; PBC: {self.ui.spin_pbc.value()}", color=GREEN)
        self.ui.but_confirm_settings.setStyleSheet('QPushButton { color: green;}')
        self.ui.but_confirm_settings.setText("Confirmed")
        self.ui.spin_straight_conc.setEnabled(True)
        self.ui.but_start_pump.setEnabled(True)
        self.ui.but_update_pump.setEnabled(True)
        self.ui.but_stop_pump.setEnabled(True)
        self.ui.spin_seg_time.setEnabled(True)
        self.ui.spin_start_conc.setEnabled(True)
        self.ui.spin_end_conc.setEnabled(True)
        self.ui.but_add_segment.setEnabled(True)
        self.ui.but_clear_segments.setEnabled(True)
        self.ui.table_segments.setEnabled(True)
        self.ui.but_start_protocol.setEnabled(True)
        self.ui.but_stop_protocol.setEnabled(True)
        self.ui.but_confirm_settings.setDisabled(True)
        self.ui.spin_start_conc.setMaximum(max(self.ui.spin_pac.value(), self.ui.spin_pbc.value()))
        self.ui.spin_end_conc.setMaximum(max(self.ui.spin_pac.value(), self.ui.spin_pbc.value()))
        self.protocol.set_dt(self.ui.spin_refresh.value())
        self.ui.spin_straight_conc.setMaximum(max(self.ui.spin_pac.value(), self.ui.spin_pbc.value()))
        self.ui.spin_seg_time.setMaximum(30)
        offset = max(self.ui.spin_pac.value(), self.ui.spin_pbc.value()) * 0.10
        self.ui.widget_plots.set_yax(min(self.ui.spin_pac.value(), self.ui.spin_pbc.value())-offset,max(self.ui.spin_pac.value(), self.ui.spin_pbc.value())+offset)

        
        
        try:
            self.port = nesp_lib.Port(self.ui.combo_com.currentText(), 19200)
            self.pumps = [nesp_lib.Pump(self.port, address=0), nesp_lib.Pump(self.port, address=1)]
        except:
            self.port = None
            self.pumps = None
            self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} @@@@@ Unable to connect to pumps! Operating in test mode @@@@@", RED)
        else:
            self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} @@@@@ PUMP CONNECTED AT COM PORT {self.ui.combo_com.currentText()} @@@@@", GREEN)
    
    def write_to_console(self, text, color=QColor(QColorConstants.Black).name()):
        
        text = f'<span style=\"white-space: pre-wrap; color: {color}\">{text}</span><br>'
        self.ui.console.moveCursor(QTextCursor.End)
        self.ui.console.insertHtml(text)
        self.ui.console.moveCursor(QTextCursor.PreviousCharacter)
    
    
    def reset_pumps(self):
        for pump in self.pumps:
            pump.reset()
    
    def update_pump(self, rates=None):
        if not rates:
            rates = self.calculate_flowrates(self.ui.spin_straight_conc.value())
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Pump flow rates are now at {rates} (ml/min)")
        
        if self.port:
            for _n, _pump in enumerate(self.pumps):
                #_pump.send_run(phases[_n])
                if rates[_n] > 0:
                    _pump.send_run()
                    _pump.pumping_rate = float(rates[_n])
        #self.ui.but_start_pump.setEnabled(True)
        #self.ui.but_update_pump.setDisabled(True)
    
    def start_pump(self):
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} PUMP START SIGNAL! Running at {self.ui.spin_straight_conc.value()} mM concentration", GREEN)
        concs = self.calculate_flowrates(self.ui.spin_straight_conc.value())
        # First, checks if pumps are running and stops them if so.
        
        if self.port:
            for _n, _pump in enumerate(self.pumps):
                if _pump.running:
                        _pump.stop()
                if concs[_n] > 0:
                        _pump.send_run()
                        _pump.pumping_rate = float(concs[_n])
                        _pump.run(wait_while_running=False)
        #self.ui.but_stop_pump.setEnabled(True)
        #self.ui.but_start_pump.setDisabled(True)
        #self.ui.but_start_protocol.setDisabled(True)
        #self.ui.but_stop_protocol.setDisabled(True)
        
    
    def stop_pump(self):
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} PUMP STOP SIGNAL!", RED)
        if self.port:
            if self.run_timer.isActive():
                for pump in self.pumps:
                    pump.stop()
                    pump.stop()
            else:
                for pump in self.pumps:
                    if pump.running:
                        pump.stop()
        #self.ui.but_stop_pump.setDisabled(True)
        #self.ui.but_start_pump.setEnabled(True)
        #self.ui.but_update_pump.setEnabled(True)
        #self.ui.but_start_protocol.setEnabled(True)
        #self.ui.but_stop_protocol.setDisabled(True)
                
    
    #def enable_update(self):
    #    if self.port:
    #        if (self.pumps[0].running or self.pumps[1].running) == False:
    #            self.ui.but_update_pump.setEnabled(True)       
    #            self.ui.but_start_pump.setDisabled(True)
    #            self.ui.but_stop_pump.setDisabled(True)
    #    else:
    #        self.ui.but_update_pump.setEnabled(True)       
    #        self.ui.but_start_pump.setDisabled(True)
    #        self.ui.but_stop_pump.setDisabled(True)
                

    
    def save_log(self):
        with open(f"./logs/{datetime.today()}_run.md", 'w') as yourFile:
            yourFile.write(str(self.ui.console.toPlainText()))
            
    def start_protocol(self):
        total_time = len(self.protocol.xvals())
        self.run_timer.start(total_time*1000)
        self.int_timer.start(self.protocol.dt()*1000)
        print("Total Time\t\tTime Left\t\tIndex\t\tSeconds")
        self.write_to_console(f"#########################################################################################################")
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Beginning protocol!")
        self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Protocol is: [Time (min), Conc In (mM), Conc Out (mM)]")
        for i, seg in self.ui.table_segments.model().get_segments().iterrows():
            self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} {seg['Time (min)']}, {seg['[Start] (mM)']}, {seg['[End] (mM)']}")
        #self.ui.but_start_protocol.setDisabled(True)
        #self.ui.but_stop_protocol.setEnabled(True)
        #self.ui.but_start_pump.setDisabled(True)
        if self.port:
            for n, pump in enumerate(self.pumps):
                # Need this?
                #if pump.running:
                #        pump.stop()
               # pump.volume_infused_clear()
                pump.run(phase=2)
    
    def timer_tick(self):
        if self.run_timer.isActive():
            total_time = len(self.protocol.xvals())
            current = self.run_timer.remainingTime()/1000
            index = int((total_time-current)/self.protocol.dt())
            if index < 0:
                # Don't allow a negative index (sometimes happens in early steps)
                index = 0
            try:
                # Do all the stuff 
                self.ui.widget_plots.set_x(self.protocol.xvals()[index])
                #print(f"{total_time}\t\t{current}\t\t{index}\t\t{self.protocol.xvals()[index]*60}\t\t{self.protocol.yvals()[index]}")

            except IndexError:
                # This is such a hacky way to end the protocol, but hey! it works. 
                #print("Run Complete")
                self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Protocol completed at {self.protocol.yvals()[-1]} mM concentration.")
                self.write_to_console(f"#########################################################################################################")
                self.ui.widget_plots.set_x(0)
                #self.ui.but_start_pump.setEnabled(True)
                #self.ui.but_stop_pump.setEnabled(True)
                #self.ui.but_update_pump.setEnabled(True)
                #self.ui.but_start_protocol.setEnabled(True)

            else:
                # If run ain't complete, keep going. 
                self.int_timer.start(self.protocol.dt()*1000)
                #self.ui.but_start_pump.setDisabled(True)
                #self.ui.but_stop_pump.setDisabled(True)
                #self.ui.but_update_pump.setDisabled(True)
    
    def stop_protocol(self):
        if self.run_timer.isActive():
            current = self.run_timer.remainingTime()/1000
            index = int((len(self.protocol.xvals())-current)/self.protocol.dt())
            self.write_to_console(f"{datetime.strftime(datetime.now(), FMT)} Protocol ended at {self.protocol.yvals()[index]} mM concentration.")
            self.stop_pump()
            self.run_timer.stop()
            self.ui.widget_plots.set_x(0)
            self.write_to_console(f"#########################################################################################################")
            #self.ui.but_start_pump.setEnabled(True)
            #self.ui.but_start_protocol.setEnabled(True)
            #self.ui.but_stop_pump.setEnabled(True)
            #self.ui.but_update_pump.setEnabled(True)
            
            
    
    def add_segment(self):
        if self.ui.spin_seg_time.value() > 0:
            self.ui.table_segments.model().add_segment([self.ui.spin_seg_time.value(), self.ui.spin_start_conc.value(), self.ui.spin_end_conc.value()])
            self.ui.spin_seg_time.setValue(0.00)
            self.ui.spin_start_conc.setValue(0)
            self.ui.spin_end_conc.setValue(0)
            self.update_pump_program()
            self.protocol.generate(self.ui.table_segments.model().get_segments())
            self.ui.widget_plots.on_change(self.protocol)
            #if self.port:
            #    if (self.pumps[0].running or self.pumps[1].running) == False:
            #        self.ui.but_start_protocol.setEnabled(True)
            #else:
            #    self.ui.but_start_protocol.setEnabled(True)
            #self.ui.table_segments.resizeColumnsToContents()
    
    def clear_segments(self):
        self.ui.table_segments.model().clear_segments()
        self.protocol.generate(self.ui.table_segments.model().get_segments())
        self.ui.widget_plots.on_change(self.protocol)
        #self.ui.but_start_protocol.setDisabled(True)
        #self.ui.but_stop_protocol.setDisabled(True)
        
    
    def update_pump_program(self):
        # converts the segments into phase format for the pumps
        # either RAT (rate) or LIN (linear ramp)
        # LIN segments have two command sets, which is reflected below. 
        prog = self.ui.table_segments.model().get_segments()
        self.phases = []
        phases_a = []
        phases_b = []
        for i, row in prog.iterrows():
            phase_a = {}
            phase_b = {}
            if row["[Start] (mM)"] == row["[End] (mM)"]:
                # if this is a "RAT" (no change)
                rates = self.calculate_flowrates(row["[Start] (mM)"])
                
                phase_a["type"] = "RAT"
                phase_a["rate"] = rates[0]
                phase_a["amt"] = float(row["Time (min)"])
                
                phase_b["type"] = "RAT"
                phase_b["rate"] = rates[1]
                phase_b["amt"] = float(row["Time (min)"])

                phases_a.append(phase_a)
                phases_b.append(phase_b)
            else:
                # if this is LIN, amounts are TIMES (minutes)
                # Time values are placed either in the first or second segment depending on length
                # First set is HR:MIN second is SEC:TENTHS
                start_rates = self.calculate_flowrates(row["[Start] (mM)"])
                end_rates = self.calculate_flowrates(row["[End] (mM)"])
                
                phase_a["type"] = "LIN"
                phase_b["type"] = "LIN"
                # make copies... 
                a_end = phase_a.copy()
                b_end = phase_b.copy()
                
                phase_a["rate"] = start_rates[0]                
                phase_b["rate"] = start_rates[1]
                a_end["rate"] = end_rates[0]
                b_end["rate"] = end_rates[1]
                
                # Time is HH:MM or SS:10THS
                
                
                if row["Time (min)"] >= 1.0:
                    time = str(int(row["Time (min)"])).zfill(2)
                    phase_a["amt"] = f"00:{time}"
                    a_end["amt"] = "00:00"
                    phase_b["amt"] = f"00:{time}"
                    b_end["amt"] = "00:00"
                elif row["Time (min)"] < 1.0:
                    time = str(int(row["Time (min)"]*60)).zfill(2)
                    phase_a["amt"] = "00:00"
                    phase_b["amt"] = "00:00"
                    a_end["amt"] = f"{time}:00"
                    b_end["amt"] = f"{time}:00"
                phases_a.append(phase_a)
                phases_b.append(phase_b)
                phases_a.append(a_end)
                phases_b.append(b_end)
        print(f"A: {phases_a}")
        print(f"B: {phases_b}")
        self.phases.append(phases_a)
        self.phases.append(phases_b)
            
        if self.port:
            for n, pump in enumerate(self.pumps):
                pump.send_program(self.phases[n])

                
                
    
    ## UTILITIES
    def calculate_flowrates(self, conc):
        # Determines the flow rates for each pump based on the pump settings.
        conc = float(conc)
        pac = float(self.ui.spin_pac.value())
        pbc = float(self.ui.spin_pbc.value())
        flow = self.ui.spin_flow_rate.value()
        # Flow rates are basically a proportion based on total flow and concs
        b_rate = ((conc - pac) / (pbc - pac)) * flow
        a_rate = flow - b_rate
        # returns the flow rates rounded to three decimal places.
        return [round(abs(a_rate), 3), round(abs(b_rate), 3)]

    ## GETTERS AND SETTERS


