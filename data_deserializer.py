from enum import Enum
from typing import Any, Tuple
from can import Message
from functools import wraps

UINT = int
CHAR = str

canMessages = {
    218099784: ['RPM', 'TPS', 'Fuel Open Time', 'Ignition Angle'],
    218100040: ['Barometer', 'MAP', 'Lambda', 'Pressure Type'],
    218100296: ['Analog Input #1', 'Analog Input #2', 'Analog Input #3', 'Analog Input #4'],
    218100552: ['Analog Input #5', 'Analog Input #6', 'Analog Input #7', 'Analog Input #8'],
    218100808: ['Frequency 1', 'Frequency 2', 'Frequency 3', 'Frequency 4'],
    218101064: ['Battery Volt', 'Air Temp', 'Coolant Temp', 'Temp Type'],
    218101320: ['Analog Input #5', 'Analog Input #7'],
    218101576: ['RPM Rate', 'TPS Rate', 'MAP Rate', 'MAF Load Rate'],
    218101832: ['Lambda #1 Measured', 'Lambda #2 Measured', 'Target Lambda'],
    218102088: [
        'PWM Duty Cycle #1', 'PWM Duty Cycle #2', 'PWM Duty Cycle #2',
        'PWM Duty Cycle #3', 'PWM Duty Cycle #4', 'PWM Duty Cycle #5',
        'PWM Duty Cycle #6', 'PWM Duty Cycle #7', 'PWM Duty Cycle #8'
    ],
    218102344: ['Percent Slip', 'Driven Wheel Rate of Change', 'Desired Value'],
    218102600: ['Driven AVG Wheel Speed', 'Non-Driven AVG Wheel Speed', 'Ignition Compensation', 'Ignitiion Cut Percentage'],
    218102856: ['Driven Wheel Speed #1', 'Driven Wheel Speed #2', 'Non-Driven Wheel Speed #1', 'Non-Driven Wheel Speed #2'],
    218103112: ['Fuel Comp-Accel', 'Fuel Comp-Starting', 'Fuel Comp-Air Temp', 'Fuel Comp-Coolant Temp'],
    218103368: ['Fuel Comp-Barometer', 'Fuel Comp-MAP'],
    # 218099784: ['Ignition Comp-Air Temp', 'Ignition Comp-Coolant Temp', 'Ignition Comp-Barometer', 'Ignition Comp-MAP'],
}


class pressure_type(Enum):
    """The pressure unit type."""
    KPA = 0
    PSI = 1


class MessageData:
    _DESERIALIZERS = []

    def __init__(self, message: Message):
        self.message = message
        self.data = message.data

    @property
    def deserializers(self):
        """List of deserializers for each message ID."""
        return type(self)._DESERIALIZERS

    @deserializers.setter
    def set_deserializers(self, deserializers):
        type(self)._DESERIALIZERS = deserializers

    def get_deserializer(self, name: str):
        """Get the deserializer for the given name."""

        for deserializer in self.deserializers:
            if deserializer['name'] == name:
                return deserializer
        print("Can't find deserializer", name)
        raise ValueError(f"Deserializer for {name} not found")

    @staticmethod
    def deserializer(
        can_id: hex,
        pname: str,
        rate: int,
        start_position: int,
        length: int,
        name: str,
        units: str,
        resolution_per_bit: float,
        data_range: Tuple[int]
    ):
        """Decorator for deserializing CAN messages.

        Args:
            can_id (hex): The CAN ID of the message.
            pname (str): PE Controller name.
            rate (int): The rate in miliseconds of data collection
            start_position (int): The position of the start byte
            length (int): The length in bytes of the data
            name (str): The human readable name of the data
            units (str): The units of the data
            resolution_per_bit (float): The level of precision of the data
            data_range (Tuple[int; 2]): The upper and lower bounds of the data
        """

        # function takes in a message object and returns the data
        def decorator(func):

            annotations = func.__annotations__

            if "return" not in annotations:
                raise ValueError("Deserializers must type hint to return a value")

            for annotation in annotations:
                if annotation not in ["message", "data", "return"]:
                    raise ValueError(f"Deserializers cannot type hint to {annotation}")

            dtype = annotations["return"]

            @wraps(func)
            def wrapper(messsage: MessageData):

                # check if function accepts a message object
                args = []
                kwargs = {}
                if "message" in annotations:
                    kwargs["message"] = messsage

                # check if function accepts a data object
                if "data" in annotations:
                    kwargs["data"] = messsage.data[obj['start_position'] - 1: obj['start_position'] + obj['length'] - 1]

                data = func(*args, **kwargs)

                # checking dtype
                if not isinstance(data, dtype):
                    raise TypeError(f"Deserializer {func.__name__} must return {dtype.__name__}")

                # checking if it matches the range
                if isinstance(data, (int, float)):
                    if not obj['data_range'][0] <= data <= obj['data_range'][1]:
                        raise ValueError(f"Data {data} is out of range {obj['data_range']}")

                return data
            obj = dict(
                can_id=can_id,
                pname=pname,
                rate=rate,
                start_position=start_position,
                length=length,
                name=name,
                units=units,
                resolution_per_bit=resolution_per_bit,
                data_range=data_range,
                dtype=dtype,
                func=wrapper
            )
            print("adding object: ", obj)
            MessageData._DESERIALIZERS.append(obj)  # pylint: disable=protected-access
            return wrapper

        return decorator

    def to_dict(self) -> dict:
        """Create a dictionary of all data points sent in the message data

        Raises:
            ValueError: If the message ID is not found in our list of deserializers

        Returns:
            Dict[]: _description_
        """
        try:
            datapoint_names = canMessages[self.message.arbitration_id]
        except KeyError:
            raise ValueError(f"Message ID {self.message.arbitration_id} not found")
        return {name: self.invoke_deserializer(name) for name in datapoint_names}

    def invoke_deserializer(self, __name: str) -> Any:
        if __name in canMessages[self.message.arbitration_id]:
            try:
                deserializer = self.get_deserializer(__name)
            except ValueError:
                pass
            else:
                return deserializer['func'](self)
        return None

# CAN Bus Detail*
# • 250 kbps Rate
# • Broadcast parameters are based on SAE Jl 939 standard
# • All 2 byte data is stored [LowByte, HighBytel
# Num = HighByte * 256 + LowByte
# • Conversion from 2 bytes to signed int is per the following:
# Num HighByte 256+LowByte
# if (Num>32767) then
# Num -Num - 65536


# CAN ID GROUP: 0xCFFF048

@MessageData.deserializer(
    can_id=0xCFFF048,
    pname='PE1',
    rate=50,
    start_position=1,
    length=2,
    name='RPM',
    units='rpm',
    resolution_per_bit=0.1,
    data_range=(0, 30000)
)
def rpm(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder='big', signed=False)


@MessageData.deserializer(
    can_id=0xCFFF048,
    pname='PE1',
    rate=50,
    start_position=3,
    length=2,
    name='TPS',
    units='%',
    resolution_per_bit=0.1,
    data_range=(0, 100),
)
def tps(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)


@MessageData.deserializer(
    can_id=0xCFFF048,
    pname='PE1',
    rate=50,
    start_position=5,
    length=2,
    name='Fuel Open Time',
    units='ms',
    resolution_per_bit=0.1,
    data_range=(0, 30),
)
def fuel_open_time(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)


@MessageData.deserializer(
    can_id=0xCFFF048,
    pname='PE1',
    rate=50,
    start_position=7,
    length=2,
    name="Ignition Angle",
    units='deg',
    resolution_per_bit=0.1,
    data_range=(-20, 100),
)
def ignition_angle(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)

# CAN ID GROUP: 0xCFFF148


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname='PE2',
    rate=50,
    start_position=1,
    length=2,
    name='Barometer',
    units='kPa',
    resolution_per_bit=0.01,
    data_range=(0, 300),
)
def barometer(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname='PE2',
    rate=50,
    start_position=3,
    length=2,
    name='MAP',
    units='kPa',
    resolution_per_bit=0.01,
    data_range=(0, 300),
)
def map_data(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname='PE2',
    rate=50,
    start_position=5,
    length=2,
    name='Lambda',
    units='lambda',
    resolution_per_bit=0.01,
    data_range=(0, 10),
)
def lambda_data(data: bytes) -> int:
    return int.from_bytes(data, byteorder='big', signed=True)


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname='PE2',
    rate=50,
    start_position=7,
    length=1,  # should be 1 bit
    name='Pressure Type',
    units='enum',
    resolution_per_bit=0.01,
    data_range=(0, 255),
)
def pressure_type_data(data: bytes) -> pressure_type:
    return pressure_type(int.from_bytes(data, byteorder='big', signed=False))
