import serial
from datetime import datetime

from PySide6.QtCore import QObject, Signal

class Meter(QObject):
    #nesp_lib is too hardcore, i'm doing it my own way
    
    measurement = Signal(tuple)
    
    def __init__(self, port=None, min_conc=0, max_conc=100, parent=None):
        self.port = port # serial.Serial('/dev/tty.usbserial-2130', 9600)
        self.min_read = None
        self.max_read = None
        self.min_conc = min_conc
        self.max_conc = max_conc
        
        self.units = 'Units'
        self._setup()
        super().__init__(parent)
        #self.units = self._get_measurement()[0][1]
        #print(self.units)
        
    def reset(self):
        self.min_read =  None
        self.max_read = None
        
    def set_min(self, val, units):
        val = float(val)
        if self.max_read != None:
            if val < self.max_read:
                if units == self.units:
                    self.min_read = val
                else:
                    print("ERROR -- UNITS DON'T MATCH OTHER SETPOINT!")
            else:
                print('ERROR -- MIN POINT GREATER THAN MAX POINT!')
        else:
            self.units = units
            self.min_read = val
    
    def set_max(self, val, units):
        val = float(val)
        if self.min_read != None:
            if val > self.min_read:
                if units == self.units:
                    self.max_read = val
                else:
                    print("ERROR -- UNITS DON'T MATCH OTHER SETPOINT!")
            else:
                print('ERROR -- MAX POINT LESS THAN MIN POINT!')
        else:
            self.units = units
            self.max_read = val
    
    def _setup(self):
        try:
            # For some reason, I'd have to hardcode the read lengths. It works in a Python Interpreter (I can use .in_waiting to get length),
            # but not here as a class for some reason. So I'm using readline instead, to be a bit safer. 
            port = serial.Serial(self.port, 9600)
            port.reset_input_buffer()
            now = f'SETRTC {datetime.now().strftime("%Y-%m-%d-%H-%M-%S-3")}\r'.encode()
            print("SETTING TIME TO: ",now)
            port.write(now)
            port.readline()
            port.readline()
            print("SERIAL CONDUCTIVITY METER INITIALIZED")
            port.close()
        except:
            print("UNABLE TO CONNECT TO CONDUCTIVITY METER!")
    
    def _get_measurement(self):
        # Returns the time and a "Measurement"
        # Measurement is (value, units)
        #print("READING!")
        if self.port is not None:
            port = serial.Serial(self.port, 9600)
            port.write(b'GETMEAS\r')
            read = port.readline()
            read = port.readline().decode()#(142).decode().split('\n')
            port.close()
            #(self.port.in_waiting).decode().split('\n')
            #print("READ: ",read)
            reply = [x.strip() for x in read.split(',')]
            #print(reply)
            time = datetime.strptime(reply[4]+" "+reply[5], '%m-%d-%Y %H:%M:%S')
            meas = (reply[9], reply[10]) # value, units    
        if self.min_read != None and self.max_read != None: 
            converted = self._convert(float(meas[0]))
            #if converted >= 0:
            meas = ("{:.2f}".format(converted), 'mM')
            #else:
                # EMIT ERROR
            #    pass
        #print((time, meas))
 
        return (time, meas)
            
               
    def _convert(self, reading):
        # Interpolation formula:
        # y = y1 + (x-x1) * ((y2-y1)/(x2-x1))
        # ys are concentrations, xs are readings
        converted = self.min_conc + (reading-self.min_read)*((self.max_conc-self.min_conc)/(self.max_read-self.min_read))
        return converted    
        
    def read(self):
        """ returns the current reading, converted if min and max are set """        
        result = self._get_measurement()
        self.measurement.emit(result)