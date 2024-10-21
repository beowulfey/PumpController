from .port import Port
from .status import Status
from .alarm_status import AlarmStatus
from .pumping_direction import PumpingDirection
from .exceptions import *

import typing
import binascii
import re
import time
import enum
import threading

# I apologize to any future reader of this code. I've never used this form of Python, have never used Typing, enums, etc. 
# Lots of new "skills" here I had to learn. It's probably butchered and ugly. 
# --AW

class Pump :
    """Pump."""

    MODEL_NUMBER_IGNORE = 0
    """Model number to ignore the model."""

    ADDRESS_DEFAULT = 0
    """Default address."""
    ADDRESS_LIMIT = 99
    """Address limit."""

    SAFE_MODE_TIMEOUT_DISABLED = 0
    """Safe mode timeout of a pump with disabled safe mode."""
    SAFE_MODE_TIMEOUT_LIMIT = 255
    """Safe mode timeout limit in units of seconds."""

    SYRINGE_DIAMETER_MINIMUM = 0.1
    """Minimum syringe diameter in units of millimeters."""
    SYRINGE_DIAMETER_MAXIMUM = 80.0
    """Maximum syringe diameter in units of millimeters."""

    PUMPING_POLL_DELAY = 0.05
    """Delay between pulling polls while waiting in units of seconds."""

    def __init__(
        self,
        port : Port,
        address : int = ADDRESS_DEFAULT,
        model_number : int = MODEL_NUMBER_IGNORE,
        safe_mode_timeout : int = SAFE_MODE_TIMEOUT_DISABLED
    ) -> None :
        """
        Constructs a pump.

        :param port:
            Port the pump is connected to.
        :param address:
            Address of the pump.
        :param model_number:
            Model number of the pump.
            If not `MODEL_NUMBER_IGNORE` and not equal to the model number of the pump
            `ModelException` is raised.
        :param safe_mode_timeout:
            Safe mode timeout of the pump in units of seconds.

        :raises ValueError:
            Address invalid.
        :raises ValueError:
            Safe mode timeout invalid.
        :raises ModelException:
            Model wrong.
        """
        if address < 0 or address > Pump.ADDRESS_LIMIT :
            raise ValueError('Address invalid: Value negative or exceeds limit.')
        self.__port = port
        self.__port_lock = threading.Lock()
        self.__address = address
        self.__safe_mode = False
        self.__heartbeat_thread : typing.Optional[threading.Thread] = None
        self.__heartbeat_event : typing.Optional[threading.Event] = None
        self.__heartbeat_event_timeout = 0.0
        self.__safe_mode_timeout_set(safe_mode_timeout, True)
        model_number_port, firmware_version_port, firmware_upgrade_port = (
            self.__firmware_version_get()
        )
        if model_number != Pump.MODEL_NUMBER_IGNORE and model_number_port != model_number :
            raise ModelException()
        self.__model_number = model_number_port
        self.__firmware_version = firmware_version_port
        self.__firmware_upgrade = firmware_upgrade_port
        
        # There is no command to just set units, so we want to save this data in pythonland
        # I've set it to ul/min by default
        # This is not at all how the original author set up this software but OH WELL
        self.__units = "UM" 

    @property
    def address(self) -> int :
        """
        Gets the address of the pump.

        Values: [`0`, `ADDRESS_LIMIT`]
        """
        return self.__address

    @property
    def model_number(self) -> int :
        """
        Gets the model number of the pump.

        Example: `1000` for NE-1000.
        """
        return self.__model_number

    @property
    def firmware_version(self) -> typing.Tuple[int, int] :
        """Gets the firmware version of the pump as major version and minor version."""
        return self.__firmware_version

    @property
    def firmware_upgrade(self) -> int :
        """
        Gets the firmware upgrade of the pump.

        Zero if the pump has no firmware upgrade.
        """
        return self.__firmware_upgrade

    @property
    def safe_mode_timeout(self) -> int :
        """
        Gets the safe mode timeout of the pump in units of seconds.

        Values: [`0`, `SAFE_MODE_TIMEOUT_LIMIT`]
        """
        _, match = self.__command_transceive(
            Pump.__CommandName.SAFE_MODE_TIMEOUT, [], Pump.__RE_PATTERN_SAFE_MODE_TIMEOUT
        )
        return int(match[1])

    @safe_mode_timeout.setter
    def safe_mode_timeout(self, safe_mode_timeout : int) -> None :
        """
        Sets the safe mode timeout of the pump in units of seconds.

        Values: [`0`, `SAFE_MODE_TIMEOUT_LIMIT`]

        A value of zero will set the communication to basic mode.
        A non-zero value will set the communication to safe mode.

        :raises ValueError:
            Safe mode timeout invalid.
        """
        self.__safe_mode_timeout_set(safe_mode_timeout)

    @property
    def status(self) -> Status :
        """Gets the status of the pump."""
        status, _ = self.__command_transceive(Pump.__CommandName.STATUS)
        return status

    @property
    def running(self) -> bool :
        """Gets if the pump is running."""
        return self.status in [Status.INFUSING, Status.WITHDRAWING, Status.PURGING]

    @property
    def syringe_diameter(self) -> float :
        """
        Gets the syringe diameter of the pump in units of millimeters.

        Values: [`SYRINGE_DIAMETER_MINIMUM`, `SYRINGE_DIAMETER_MAXIMUM`]
        """
        _, match = self.__command_transceive(
            Pump.__CommandName.SYRINGE_DIAMETER, [], Pump.__RE_PATTERN_SYRINGE_DIAMETER
        )
        return float(match[1])

    @syringe_diameter.setter
    def syringe_diameter(self, syringe_diameter : float) -> None :
        """
        Sets the syringe diameter of the pump in units of millimeters.

        Values: [`SYRINGE_DIAMETER_MINIMUM`, `SYRINGE_DIAMETER_MAXIMUM`]

        This value dictates the minimum and maximum pumping rate of the pump.

        Note: The value is truncated to the 4 most significant digits.

        :raises ValueError:
            Syringe diameter invalid.
        """
        if (
            syringe_diameter < Pump.SYRINGE_DIAMETER_MINIMUM or
            syringe_diameter > Pump.SYRINGE_DIAMETER_MAXIMUM
        ) :
            raise ValueError('Syringe diameter invalid: Value exceeds limit.')
        self.__command_transceive(Pump.__CommandName.SYRINGE_DIAMETER, [syringe_diameter])

    @property
    def pumping_direction(self) -> PumpingDirection :
        """Gets the pumping direction of the pump."""
        _, pumping_direction_string = self.__command_transceive(
            Pump.__CommandName.PUMPING_DIRECTION
        )
        pumping_direction = Pump.__PUMPING_DIRECTION_EXTERNAL.get(pumping_direction_string)
        if pumping_direction is None :
            raise InternalException()
        return pumping_direction

    @pumping_direction.setter
    def pumping_direction(self, pumping_direction : PumpingDirection) -> None :
        """Sets the pumping direction of the pump."""
        pumping_direction_string = Pump.__PUMPING_DIRECTION_INTERNAL.get(pumping_direction)
        if pumping_direction_string is None :
            raise ValueError('Pumping direction invalid: Value unknown.')
        self.__command_transceive(Pump.__CommandName.PUMPING_DIRECTION, [pumping_direction_string])

    ###########################################################################
    # THINGS IN HERE USE UNITS AND NEED UPDATING

    @property
    def pumping_volume(self) -> float :
        """Gets the pumping volume of the pump in units of microliters."""
        _, match = self.__command_transceive(
            Pump.__CommandName.PUMPING_VOLUME, [], Pump.__RE_PATTERN_PUMPING_VOLUME
        )
        value = float(match[1])
        units = match[2]
        value_microliters = Pump.__VOLUME_MICROLITERS.get(units)
        if value_microliters is None :
            raise InternalException()
        return value_microliters(value)

    @pumping_volume.setter
    # NEED TO UPDATE THIS
    def pumping_volume(self, pumping_volume : float) -> None :
        """
        Sets the pumping volume of the pump in units of microliters.

        Note: The value is truncated to the 4 most significant digits.

        :raises ValueError:
            Pumping volume invalid.
        """
        
        #if pumping_volume < 0.001 / 1_000.0 or pumping_volume >= 10_000.0 :
        #    raise ValueError('Pumping volume invalid: Value exceeds limit.')
        #if pumping_volume >= 10_000.0 / 1_000.0 :
        #    units = 'ML'
        #else :
        #    pumping_volume *= 1_000.0
        #    units = 'UL'
        self.__command_transceive(Pump.__CommandName.PUMPING_VOLUME, [self.__units])
        try :
            self.__command_transceive(Pump.__CommandName.PUMPING_VOLUME, [pumping_volume])
        except ValueError :
            raise ValueError('Pumping volume invalid WHOOPS.')

    @property
    def pumping_rate(self) -> float :
        """Gets the pumping rate of the pump in units of microliters per minute."""
        _, match = self.__command_transceive(
            Pump.__CommandName.PUMPING_RATE, [], Pump.__RE_PATTERN_PUMPING_RATE
        )
        value = float(match[1])
        units = match[2]
        value_microliters_per_minute = Pump.__PUMPING_RATE_MICROLITERS_PER_MINUTE.get(units)
        if value_microliters_per_minute is None :
            raise InternalException()
        return value_microliters_per_minute(value)

    @pumping_rate.setter
    def pumping_rate(self, pumping_rate : float) -> None :
        """
        Sets the pumping rate of the pump in units specified.

        Equivalent to the RAT command. 

        :raises ValueError:
            Pumping rate invalid.
        """

        try :
            self.__command_transceive(Pump.__CommandName.PUMPING_RATE, [pumping_rate, self.__units])
        except ValueError :
            raise ValueError('Pumping rate invalid: Value exceeds limit.')

    @property
    def volume_infused(self) -> float :
        """Gets the volume infused of the pump in units of milliliters."""
        return self.__dispensation_get(False)

    def volume_infused_clear(self) -> None :
        """Sets the volume infused of the pump to zero."""
        self.__command_transceive(
            Pump.__CommandName.DISPENSATION_CLEAR, [Pump.__PumpingDirectionInfuse]
        )

    @property
    def volume_withdrawn(self) -> float :
        """Gets the volume withdrawn of the pump in units of milliliters."""
        return self.__dispensation_get(True)

    def volume_withdrawn_clear(self) -> None :
        """Sets the volume withdrawn of the pump to zero."""
        self.__command_transceive(
            Pump.__CommandName.DISPENSATION_CLEAR, [Pump.__PumpingDirectionWithdraw]
        )

    def reset(self) -> None : 
        # Don't use this unless you really have to! 
        # It erases the network addresses too! 
        self.__command_transceive(Pump.__CommandName.RESET)
    
    def send_run (self, wait_while_running : bool = False) -> None :
        self.__command_transceive(Pump.__CommandName.PHASE, [1])
        self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.PUMPING_RATE.value])
        self.__command_transceive(Pump.__CommandName.PUMPING_DIRECTION, [Pump.__PumpingDirectionInfuse])
            
            
    def send_program(self, prog : list , wait_while_running : bool = True) -> None : 
        print(f"SEND PROGRAM TO PUMP {self.address}")
        # This command converts a list of program steps into phases on the pump
        if prog != []:
            count = 0
            offset = 0
            for n, phase in enumerate(prog):
                # program offset. #1 is base run, #3 is beginning of programs. 
                # add 1 to convert from index-0, add 1 to skip past the first phase (continuous run)
                n = n + 1 + 1
                
                self.__command_transceive(Pump.__CommandName.PHASE, [n+offset])
                
                if phase["type"] == "RAT": 
                    if phase["rate"] == 0:
                        #time = str(int(phase["amt"]*60)).zfill(2)
                        # if the calculated flow rate is zero, replace this segment with a system pause
                        # this is only an issue with flat rates. 
                        # convert time to seconds
                        # then add more phases for pauses if needed 
                        time = int(phase["amt"]*60)
                        while time > 99:
                            self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.PAUSE.value, 99])
                            offset += 1
                            self.__command_transceive(Pump.__CommandName.PHASE, [n+offset])
                            #offset += 1
                            time = time - 99
                        self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.PAUSE.value, str(time).zfill(2)])
                    else:
                        # if this is a flat volume, calculate the volume needed and send it as a RAT function
                        vol = phase["amt"]*phase["rate"]
                        self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.PUMPING_RATE.value])
                        self.__command_transceive(Pump.__CommandName.PUMPING_RATE, [phase["rate"], self.__units])
                        self.__command_transceive(Pump.__CommandName.PUMPING_VOLUME, [vol])
                        self.__command_transceive(Pump.__CommandName.PUMPING_DIRECTION, [Pump.__PumpingDirectionInfuse])
                        
                else:
                    # if phase is LIN
                    self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.LINEAR.value])
                    self.__command_transceive(Pump.__CommandName.PUMPING_RATE, [phase["rate"], self.__units])
                    self.__command_transceive(Pump.__CommandName.TIME, phase["amt"])
                    self.__command_transceive(Pump.__CommandName.PUMPING_DIRECTION, [Pump.__PumpingDirectionInfuse])
                count = n + 1 + 1 + offset
            self.__command_transceive(Pump.__CommandName.PHASE, [n+offset+1])
            self.__command_transceive(Pump.__CommandName.FUNC, [Pump.__CommandName.STOP.value])
        if wait_while_running :
            self.wait_while_running()
            #self.__command_transceive(Pump.__CommandName.PHASE, [1])
    
    def run(self, phase : int = 1, wait_while_running : bool = False) -> None :
        self.__command_transceive(Pump.__CommandName.RUN, [phase])
        if wait_while_running :
            self.wait_while_running()
    
    def run_purge(self) -> None :
        """
        Runs the pump considering the direction set at maximum rate.

        Running will continue until stopped.
        """
        self.__command_transceive(Pump.__CommandName.RUN_PURGE)

    def stop(self, wait_while_running : bool = True) -> None :
        """
        Stops the pump.

        :param wait_while_running:
            If the function waits while the pump is running.
        """
        self.__command_transceive(Pump.__CommandName.STOP)
        if wait_while_running :
            self.wait_while_running()

    def wait_while_running(self) -> None :
        """Waits while the pump is running."""
        while self.running :
            time.sleep(Pump.PUMPING_POLL_DELAY)

    # Start transmission
    __STX = 0x02
    # End transmission
    __ETX = 0x03

    class __CommandName(str, enum.Enum) :
        STATUS             = ''
        SAFE_MODE_TIMEOUT  = 'SAF'
        FIRMWARE_VERSION   = 'VER'
        SYRINGE_DIAMETER   = 'DIA'
        PUMPING_DIRECTION  = 'DIR'
        PUMPING_VOLUME     = 'VOL'
        PUMPING_RATE       = 'RAT'
        DISPENSATION       = 'DIS'
        DISPENSATION_CLEAR = 'CLD'
        RUN                = 'RUN'
        RUN_PURGE          = 'PUR'
        STOP               = 'STP'
        RESET              = 'RESET'
        PHASE              = 'PHN'
        FUNC               = 'FUN'
        PAUSE              = 'PAS'
        TIME               = 'TIM'
        LINEAR             = 'LIN'

    __STATUS = {
        'I' : Status.INFUSING,
        'W' : Status.WITHDRAWING,
        'X' : Status.PURGING,
        'S' : Status.STOPPED,
        'P' : Status.PAUSED,
        'T' : Status.SLEEPING,
        'U' : Status.WAITING
    }

    __STATUS_ALARM = 'A'

    __ALARM_STATUS = {
        'R' : AlarmStatus.RESET,
        'S' : AlarmStatus.STALLED,
        'T' : AlarmStatus.TIMEOUT,
        'E' : AlarmStatus.ERROR,
        'O' : AlarmStatus.RANGE
    }

    # Regular expressions.
    __RE_INTEGER = r'(\d+)'
    __RE_FLOAT   = r'(\d+\.\d*)'
    __RE_SYMBOL  = '([A-Z]+)'

    # Format: "NE" <Model number> ("X" (<Firmware upgrade>)?)? "V"
    # <Firmware major version> "." <Firmware minor version>
    __RE_PATTERN_FIRMWARE_VERSION = re.compile(
        'NE' + __RE_INTEGER + '(X' + __RE_INTEGER + '?)?' + 'V' +
        __RE_INTEGER + r'\.' + __RE_INTEGER,
        re.ASCII
    )
    __RE_PATTERN_SAFE_MODE_TIMEOUT = re.compile(__RE_INTEGER, re.ASCII)
    __RE_PATTERN_SYRINGE_DIAMETER = re.compile(__RE_FLOAT, re.ASCII)
    # Format: <Pumping volume> <Units>
    __RE_PATTERN_PUMPING_VOLUME = re.compile(__RE_FLOAT + __RE_SYMBOL, re.ASCII)
    # Format: <Pumping rate> <Units>
    __RE_PATTERN_PUMPING_RATE = re.compile(__RE_FLOAT + __RE_SYMBOL, re.ASCII)
    # Format: "I" <Volume infused> "W" <Volume withdrawn> <Units>
    __RE_PATTERN_DISPENSATION = re.compile('I' + __RE_FLOAT + 'W' + __RE_FLOAT + __RE_SYMBOL)

    __PumpingDirectionInfuse   = 'INF'
    __PumpingDirectionWithdraw = 'WDR'

    __PUMPING_DIRECTION_EXTERNAL = {
        __PumpingDirectionInfuse : PumpingDirection.INFUSE,
        __PumpingDirectionWithdraw : PumpingDirection.WITHDRAW
    }

    __PUMPING_DIRECTION_INTERNAL = {
        pumping_direction_external : pumping_direction_internal
        for pumping_direction_internal, pumping_direction_external in
        __PUMPING_DIRECTION_EXTERNAL.items()
    }

    __PUMPING_RATE_MILLILITERS_PER_MINUTE = {
        # Milliliters per minute.
        'MM' : lambda value : value,
        # Milliliters per hour.
        'MH' : lambda value : value / 60.0,
        # Microliters per minute.
        'UM' : lambda value : value / 1_000.0,
        # Microliters per hour.
        'UH' : lambda value : value / 60_000.0,
    }
    
    __PUMPING_RATE_MICROLITERS_PER_MINUTE = {
        # Milliliters per minute.
        'MM' : lambda value : value * 1_000.0,
        # Milliliters per hour.
        'MH' : lambda value : value * 60_000.0,
        # Microliters per minute.
        'UM' : lambda value : value,
        # Microliters per hour.
        'UH' : lambda value : value / 60.0,
        # Nanoliters per minute.
        'NM' : lambda value : value / 1_000.0,
        # Nanoliters per hour.
        'NH' : lambda value: value / 60_000.0,
    }

    __VOLUME_MILLILITERS = {
        # Milliliters.
        'ML' : lambda value : value,
        # Microliters.
        'UL' : lambda value : value / 1_000.0,
    }

    __VOLUME_MICROLITERS = {
        # Milliliters.
        'ML' : lambda value : value * 1_000.0,
        # Microliters.
        'UL' : lambda value : value,
        # Nanoliters.
        'NL' : lambda value : value / 1_000.0,
    }

    __VOLUME_MILLILITERS_SET = {
        # Milliliters.
        'ML' : lambda value : value,
        # Microliters.
        'UL' : lambda value : value * 1_000.0,
    }
    
    __VOLUME_MICROLITERS_SET = {
        # Milliliters.
        'ML' : lambda value : value * 1_000.0,
        # Microliters.
        'UL' : lambda value : value,
        # Nanoliters.
        'NH' : lambda value : value / 1_000.0,
    }

    def __error_handle_not_applicable() -> None :
        raise StateException()

    def __error_handle_out_of_range() -> None :
        raise ValueError()

    def __error_handle_communication() -> None :
        raise ChecksumRequestException()

    def __error_handle_ignored() -> None :
        pass

    __ERROR = {
        # Not applicable.
        'NA'  : __error_handle_not_applicable,
        # Out of range.
        'OOR' : __error_handle_out_of_range,
        # Communication.
        'COM' : __error_handle_communication,
        # Ignored.
        'IGN' : __error_handle_ignored
    }

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

    @staticmethod
    def __command_checksum_calculate(data : bytes) -> int :
        """Gets the CCITT-CRC of the given data."""
        return binascii.crc_hqx(data, 0x0000)

    @staticmethod
    def __command_request_format(
        address : int,
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = []
    ) -> str :
        return str(address) + name.value + ''.join(
            Pump.__ARGUMENT[type(argument)](argument)
            for argument in arguments
        )

    @classmethod
    def __command_reply_parse(
        cls,
        address : int,
        data_string : str
    ) -> typing.Tuple[Status, typing.Optional[AlarmStatus], str] :
        data_length = len(data_string)
        if data_length < 3 :
            raise InternalException()
        address_string = data_string[0 : 2]
        address_ = int(address_string)
        if address_ != address :
            raise AddressException()
        status_string = data_string[2]
        if status_string == cls.__STATUS_ALARM :
            if data_string[3] != '?' :
                raise InternalException()
            alarm_status_string = data_string[4]
            alarm_status = cls.__ALARM_STATUS.get(alarm_status_string)
            if alarm_status is None :
                raise InternalException()
            return Status.STOPPED, alarm_status, ''
        status = cls.__STATUS.get(status_string)
        if status is None :
            raise InternalException()
        result = data_string[3 : data_length]
        if result and result[0] == '?' :
            error_string = result[1 :]
            error = cls.__ERROR.get(error_string)
            if error is None :
                raise InternalException()
            error()
        return status, None, result

    @classmethod
    def __command_request_encode_basic(
        cls,
        request : str
    ) -> bytes :
        request += '\r'
        return request.encode()

    @classmethod
    def __command_request_encode_safe(
        cls,
        request : str
    ) -> bytes :
        request_bytes = request.encode()
        checksum = cls.__command_checksum_calculate(request_bytes)
        return bytes([
            cls.__STX,
            # Length (1 byte) + Checksum (2 bytes) + ETX (1 byte) = 4 bytes
            len(request_bytes) + 4,
            *request_bytes,
            *checksum.to_bytes(2, byteorder = 'big', signed = False),
            cls.__ETX
        ])

    @classmethod
    def __command_reply_receive_port_basic(cls, port : Port) -> str :
        data = port._receive(1)
        if data[0] != cls.__STX :
            raise InternalException()
        data = bytearray()
        while True :
            data_length = max(1, port._waiting_receive)
            data.extend(port._receive(data_length))
            if data[-1] == cls.__ETX :
                del data[-1]
                break
        data_string = data.decode()
        return data_string

    @classmethod
    def __command_reply_receive_port_safe(cls, port : Port) -> str :
        data_header = port._receive(2)
        if data_header[0] != cls.__STX :
            raise InternalException()
        data_length = data_header[1]
        if data_length <= 2 :
            raise InternalException()
        data = port._receive(data_length - 1)
        if data[-1] != cls.__ETX :
            raise InternalException()
        checksum = int.from_bytes(data[-3 : -1], byteorder = 'big', signed = False)
        data = data[0 : -3]
        if checksum != cls.__command_checksum_calculate(data) :
            raise ChecksumReplyException()
        data_string = data.decode()
        return data_string

    @classmethod
    def __command_transceive_port(
        cls,
        port : Port,
        safe_mode_transmit : bool,
        safe_mode_receive : bool,
        address : int,
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = [],
        re_pattern_result : typing.Optional[re.Pattern] = None,
        alarm_ignore : bool = False
    ) -> typing.Tuple[Status, typing.Union[str, re.Match]] :
        while True :
            request = cls.__command_request_format(address, name, arguments)
            if safe_mode_transmit :
                request_bytes = cls.__command_request_encode_safe(request)
            else :
                request_bytes = cls.__command_request_encode_basic(request)
            port._transmit(request_bytes)
            if safe_mode_receive :
                reply = cls.__command_reply_receive_port_safe(port)
            else :
                reply = cls.__command_reply_receive_port_basic(port)
            status, alarm, result = cls.__command_reply_parse(address, reply)
            if alarm is not None and alarm_ignore :
                alarm_ignore = False
            else :
                break
        if alarm is not None :
            raise StatusAlarmException(alarm)
        if re_pattern_result is None :
            return status, result
        match = re_pattern_result.fullmatch(result)
        if match is None :
            raise InternalException()
        return status, match

    def __command_transceive(
        self,
        name : __CommandName,
        arguments : typing.Iterable[typing.Union[str, int, float]] = [],
        re_pattern_result : typing.Optional[re.Pattern] = None,
        safe_mode_transmit : typing.Optional[bool] = None,
        safe_mode_receive : typing.Optional[bool] = None,
        alarm_ignore : bool = False
    ) -> typing.Tuple[Status, typing.Union[str, re.Match]] :
        if safe_mode_transmit is None :
            safe_mode_transmit = self.__safe_mode
        if safe_mode_receive is None :
            safe_mode_receive = safe_mode_transmit
        with self.__port_lock :
            print(f"PUMP TRANSMIT: {self.__address} {name.value} {[r for r in arguments]}")
            reply = Pump.__command_transceive_port(
                self.__port,
                safe_mode_transmit,
                safe_mode_receive,
                self.__address,
                name,
                arguments,
                re_pattern_result,
                alarm_ignore
            )
        if self.__heartbeat_event is not None :
            self.__heartbeat_event.set()
        
        return reply

    def __safe_mode_timeout_set(self, safe_mode_timeout : int, initial : bool = False) -> None :
        if safe_mode_timeout < 0 or safe_mode_timeout > Pump.SAFE_MODE_TIMEOUT_LIMIT :
            raise ValueError('Safe mode timeout invalid: Value negative or exceeds limit.')
        safe_mode = safe_mode_timeout != 0
        self.__command_transceive(
            Pump.__CommandName.SAFE_MODE_TIMEOUT, [safe_mode_timeout],
            safe_mode_transmit = True, safe_mode_receive = safe_mode, alarm_ignore = initial
        )
        self.__safe_mode = safe_mode
        self.__heartbeat_setup(float(safe_mode_timeout))

    def __heartbeat_setup(self, timeout_seconds : float) -> None :
        activate = timeout_seconds != 0
        active = self.__heartbeat_thread is not None
        self.__heartbeat_event_timeout = timeout_seconds / 2
        if activate == active :
            if activate :
                self.__heartbeat_event.set()
            return
        if activate :
            self.__heartbeat_thread = threading.Thread(
                target = self.__heartbeat,
                daemon = True
            )
            self.__heartbeat_event = threading.Event()
            self.__heartbeat_thread.start()
        else :
            self.__heartbeat_event.set()
            self.__heartbeat_thread.join()
            self.__heartbeat_event = None
            self.__heartbeat_thread = None

    def __heartbeat(self) -> None :
        while self.__heartbeat_event_timeout != 0.0 :
            if self.__heartbeat_event.wait(self.__heartbeat_event_timeout) :
                self.__heartbeat_event.clear()
            else :
                self.__command_transceive(Pump.__CommandName.STATUS)

    def __firmware_version_get(self) -> typing.Tuple[int, typing.Tuple[int, int], int] :
        _, match = self.__command_transceive(
            Pump.__CommandName.FIRMWARE_VERSION, [], Pump.__RE_PATTERN_FIRMWARE_VERSION
        )
        model_number = int(match[1])
        upgrade = 0 if match[2] is None else 1 if match[3] is None else int(match[3])
        version_major = int(match[4])
        version_minor = int(match[5])
        return model_number, (version_major, version_minor), upgrade

    def __dispensation_get(self, withdrawn : bool) -> float :
        _, match = self.__command_transceive(
            Pump.__CommandName.DISPENSATION, [], Pump.__RE_PATTERN_DISPENSATION
        )
        value = float(match[1 + withdrawn])
        units = match[3]
        value_milliliters = Pump.__VOLUME_MILLILITERS.get(units)
        if value_milliliters is None :
            raise InternalException()
        return value_milliliters(value)