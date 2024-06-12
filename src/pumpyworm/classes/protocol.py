import pandas as pd
import numpy as np

class Protocol:
    def __init__(self):
        self._dt = 0.5
        self._segs = {}
        self._xvals = []
        self._yvals = []
        self.generate()
        
    def set_dt(self, dt):
        self._dt = dt
        self.generate()
        
    def dt(self):
        return self._dt
    
    def xvals(self):
        return self._xvals
    
    def set_xvals(self, x):
        self._xvals = x
    
    def yvals(self):
        return self._yvals
    
    def set_yvals(self, y):
        self._yvals = y
     
    def generate(self, segs: pd.DataFrame = None ):
        if segs is not None:
            
            xtot = []
            ytot = []
            total_time = 0
            for i, seg in segs.iterrows():
                x = [total_time, total_time + seg.to_list()[0]]
                y = [seg.to_list()[1], seg.to_list()[2]]
                steps = int(seg.to_list()[0]*60 / self._dt)  # Locked at 1 second now.
                x_expanded = np.linspace(x[0], x[1], steps+1, endpoint=True)
                y_expanded = np.interp(x_expanded, x, y)
                xtot = xtot + x_expanded.tolist()
                ytot = ytot + y_expanded.tolist()
                total_time += seg.to_list()[0]
            self._xvals = xtot
            self._yvals = ytot