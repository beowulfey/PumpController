from .port import Port
from .exceptions import *

import typing
import binascii
import re
import time
import enum
import threading

# My hacky duplicate of the "Pump" class for use with an Orion Lab Star EC112 conductivity meter. 

class Meter :
    def __init__( self, port : Port ) -> None :
        """
        Constructs a meter.

        :param port:
            Port the meter is connected to.
        :param units: 
            Units measurement (either conductivity or concentration)
        """
        self.__port = port
        self.__port_lock = threading.Lock()
        self.__units = "mS/cm"
        
        # STARTUP:
        # SETCSV
        # SETMODE COND
        # SETRTC 
        
    # Start transmission
    __STX = 0x02
    # End transmission
    __ETX = 0x03
    
    class __CommandName(str, enum.Enum) :
        # These commands are taken from the EC112 manual. 
        MEASURE             = 'GETMEAS'
        CSVSET              = 'SETCSV'
        MODESET             = 'SETMODE'
        TIMESET             = 'SETRTC'
        
    def __argument_str(value : str) -> str :
        return value

    def __argument_int(value : int) -> str :
        return str(value)

    def __argument_float(value : float) -> str :
        # From the docs: Maximum of 4 digits plus 1 decimal point. Maximum of 3 digits to the right
        # of the decimal point.
        if value.is_integer() :
            return str(int(value))
        value_string = str(value)
        if len(value_string) > 5 :
            value_string = value_string[0 : 5]
        return value_string

    __ARGUMENT = {
        str   : __argument_str,
        int   : __argument_int,
        float : __argument_float
    }
    
    def measure(self) -> str :
        result = self.__command_transceive(Meter.__CommandName.MEASURE, [])
        print(result)
    
    @staticmethod
    def __command_request_format(
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = []
    ) -> str :
        sent = '>' + name.value + ''.join(
            Meter.__ARGUMENT[type(argument)](argument)
            for argument in arguments
        )
        print(sent)
        return sent
        
    @classmethod
    def __command_request_encode_basic( cls, request : str ) -> bytes :
        request += '\r'
        print(request.encode())
        return request.encode()
    
    
    @classmethod
    def __command_reply_receive_port_basic(cls, port : Port) -> str :
        echo_len = port._waiting_receive
        print(echo_len)
        echo = port._receive(echo_len)
        print("ECHO:", echo)
        data_len = port._waiting_receive
        print(data_len)
        if data_len > 0 :
            data = port._receive(data_len)
        else:
            data = None
        print(data.decode())
        data_string = data.decode()
        return data_string
    
    @classmethod
    def __command_transceive_port(
        cls,
        port : Port,
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = [],
    ) -> str :
        request = cls.__command_request_format(name, arguments)
        request_bytes = cls.__command_request_encode_basic(request)
        print("REQUEST", request_bytes)
        port._transmit(request_bytes)
        result = cls.__command_reply_receive_port_basic(port)
        return result
    
    def __command_transceive(
        self,
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = [],
    ) -> str :
        with self.__port_lock :
            print(f"TRANSMIT: {name.value} {[r for r in arguments]}")
            reply = Meter.__command_transceive_port(
                self.__port,
                name,
                arguments
            )
        
        return reply