from enum import Enum
from typing import Any, Tuple
from can import Message
from functools import wraps
from decimal import Decimal

UINT = int
CHAR = str

canMessages = {
    218099784: ["RPM", "TPS", "Fuel Open Time", "Ignition Angle"],
    218100040: ["Barometer", "MAP", "Lambda", "Pressure Type"],
    218100296: [
        "Analog Input #1",
        "Analog Input #2",
        "Analog Input #3",
        "Analog Input #4",
    ],
    218100552: [
        "Analog Input #5",
        "Analog Input #6",
        "Analog Input #7",
        "Analog Input #8",
    ],
    218100808: ["Frequency 1", "Frequency 2", "Frequency 3", "Frequency 4"],
    218101064: ["Battery Volt", "Air Temp", "Coolant Temp", "Temp Type"],
    218101320: ["Analog Input #5", "Analog Input #7"],
    218101576: ["RPM Rate", "TPS Rate", "MAP Rate", "MAF Load Rate"],
    218101832: ["Lambda #1 Measured", "Lambda #2 Measured", "Target Lambda"],
    218102088: [
        "PWM Duty Cycle #1",
        "PWM Duty Cycle #2",
        "PWM Duty Cycle #2",
        "PWM Duty Cycle #3",
        "PWM Duty Cycle #4",
        "PWM Duty Cycle #5",
        "PWM Duty Cycle #6",
        "PWM Duty Cycle #7",
        "PWM Duty Cycle #8",
    ],
    218102344: ["Percent Slip", "Driven Wheel Rate of Change", "Desired Value"],
    218102600: [
        "Driven Avg Wheel Speed",
        "Non-Driven Avg Wheel Speed",
        "Ignition Compensation",
        "Ignition Cut Percentage",
    ],
    218102856: [
        "Driven Wheel Speed #1",
        "Driven Wheel Speed #2",
        "Non-Driven Wheel Speed #1",
        "Non-Driven Wheel Speed #2",
    ],
    218103112: [
        "Fuel Comp-Accel",
        "Fuel Comp-Starting",
        "Fuel Comp-Air Temp",
        "Fuel Comp-Coolant Temp",
    ],
    218103368: ["Fuel Comp-Barometer", "Fuel Comp-MAP"],

} # Wait, was there not supposed to be a bracket here??? - Gino

class pressure_type(Enum):
    """The pressure unit type."""

    KPA = 0
    PSI = 1

    def __str__(self):
        return self.name


class temp_type(Enum):
    """The temperature unit type."""

    C = 0
    F = 1

    def __str__(self):
        return self.name

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
            if deserializer["name"] == name:
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
        data_range: Tuple[int],
        units: str = None,
        resolution_per_bit: float = None,
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
                    kwargs["data"] = messsage.data[
                        obj["start_position"]
                        - 1 : obj["start_position"]
                        + obj["length"]
                        - 1
                    ]

                data = func(*args, **kwargs)

                if resolution := obj.get("resolution_per_bit"):
                    # decimal safe multiplication (no 0.1 + 0.2)

                    d_data = Decimal(data)
                    d_res = d_data * Decimal(resolution)
                    if int(d_res) == float(d_res):
                        data = int(d_res)
                    else:
                        data = float(d_res)

                    data = round(data, 2) if isinstance(data, float) else data

                # checking dtype
                # if not isinstance(data, dtype):
                #     raise TypeError(f"Deserializer {func.__name__} must return {dtype.__name__}")

                # checking if it matches the range
                if isinstance(data, (int, float)):
                    if not obj["data_range"][0] <= data <= obj["data_range"][1]:
                        ...
                        # raise ValueError(
                        #     f"Data {data} is out of range {obj['data_range']} while processing metric {obj['name']}"
                        # )
                        print(
                            f"Data {data} is out of range {obj['data_range']} while processing metric {obj['name']}"
                        )

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
                func=wrapper,
            )
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
                return deserializer["func"](self)
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

#////////////////above is original code-------------------------------------------------


#--------------------------------------------------------------------------------------

@MessageData.deserializer(
    can_id=0xCFFF748,
    pname="PE8",
    rate=100,
    start_position=1,
    length=2,
    name="RPM Rate",
    units="rpm/sec",
    resolution_per_bit=1,
    data_range=(-10000, 10000),
)
def rpm(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFF748,
    pname="PE8",
    rate=100,
    start_position=3,
    length=2,
    name="TPS Rate",
    units="%/sec",
    resolution_per_bit=1,
    data_range=(-3000, 3000),
)
def tps(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFF748,
    pname="PE8",
    rate=100,
    start_position=5,
    length=2,
    name="MAP Rate",
    units="psi/sec",
    resolution_per_bit=1,
    data_range=(-300, 300),
)
def map_rate(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFA48,
    pname="PE11",
    rate=100,
    start_position=1,
    length=2,
    name="Percent Slip",
    units="%",
    resolution_per_bit=0.1,
    data_range=(-3000, 3000),
)
def slip(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFB48,
    pname="PE12",
    rate=100,
    start_position=1,
    length=2,
    name="Driven Avg Wheel Speed",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def driven_avg_wheel_speed(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFB48,
    pname="PE12",
    rate=100,
    start_position=3,
    length=2,
    name="Non-Driven Avg Wheel Speed",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def non_driven_avg_wheel_speed(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFB48,
    pname="PE12",
    rate=100,
    start_position=5,
    length=2,
    name="Ignition Compensation",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(0, 100),
)
def ignition_comp(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFB48,
    pname="PE12",
    rate=100,
    start_position=7,
    length=2,
    name="Ignition Cut Percentage",
    units="%",
    resolution_per_bit=1,
    data_range=(0, 100),
)
def ignition_cut(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFC48,
    pname="PE13",
    rate=100,
    start_position=1,
    length=2,
    name="Driven Wheel Speed #1",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def wheel_speed_1(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFC48,
    pname="PE13",
    rate=100,
    start_position=3,
    length=2,
    name="Driven Wheel Speed #2",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def wheel_speed_2(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFC48,
    pname="PE13",
    rate=100,
    start_position=5,
    length=2,
    name="Non-Driven Wheel Speed #1",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def wheel_non_speed_1(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFC48,
    pname="PE13",
    rate=100,
    start_position=7,
    length=2,
    name="Non-Driven Wheel Speed #2",
    units="ft/sec",
    resolution_per_bit=0.1,
    data_range=(0, 3000),
)
def wheel_non_speed_2(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)

@MessageData.deserializer(
    can_id=0xCFFFD48,
    pname="PE14",
    rate=100,
    start_position=1,
    length=2,
    name="Fuel Comp - Acceleration",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 500),
)
def fuel_comp_accel(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFD48,
    pname="PE14",
    rate=100,
    start_position=3,
    length=2,
    name="Fuel Comp - Starting",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 500),
)
def fuel_comp_starting(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFD48,
    pname="PE14",
    rate=100,
    start_position=5,
    length=2,
    name="Fuel Comp - Air Temp",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 500),
)
def fuel_comp_air_temp(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFD48,
    pname="PE14",
    rate=100,
    start_position=7,
    length=2,
    name="Fuel Comp - Coolant Temp",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 500),
)
def fuel_comp_coolant_temp(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFFE48,
    pname="PE15",
    rate=100,
    start_position=3,
    length=2,
    name="Fuel Comp - MAP",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 500),
)
def fuel_comp_map(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFD048,
    pname="PE16",
    rate=100,
    start_position=1,
    length=2,
    name="Ignition Comp - Air Temp",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(-20, 20),
)
def ignition_comp_air_temp(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFD048,
    pname="PE16",
    rate=100,
    start_position=3,
    length=2,
    name="Ignition Comp - Coolant Temp",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(-20, 20),
)
def ignition_comp_coolant_temp(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFD048,
    pname="PE16",
    rate=100,
    start_position=5,
    length=2,
    name="Ignition Comp - Barometer",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(-20, 20),
)
def ignition_comp_barometer(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

@MessageData.deserializer(
    can_id=0xCFFD048,
    pname="PE16",
    rate=100,
    start_position=7,
    length=2,
    name="Ignition Comp - MAP",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(-20, 20),
)
def ignition_comp_map(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=True)

#////////////////////////////////////////////////////below is original code

@MessageData.deserializer(
    can_id=0xCFFF048,
    pname="PE1",
    rate=50,
    start_position=1,
    length=2,
    name="RPM",
    units="rpm",
    resolution_per_bit=1,
    data_range=(0, 30000),
)
def rpm(data: bytes) -> UINT:  # data is an unsigned int
    return int.from_bytes(data, byteorder="little", signed=False)


@MessageData.deserializer(
    can_id=0xCFFF048,
    pname="PE1",
    rate=50,
    start_position=3,
    length=2,
    name="TPS",
    units="%",
    resolution_per_bit=0.1,
    data_range=(0, 100),
)
def tps(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)



@MessageData.deserializer(
    can_id=0xCFFF048,
    pname="PE1",
    rate=50,
    start_position=5,
    length=2,
    name="Fuel Open Time",
    units="ms",
    resolution_per_bit=0.01,  # CHANGED FROM PE3
    data_range=(0, 30),
)
def fuel_open_time(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)



@MessageData.deserializer(
    can_id=0xCFFF048,
    pname="PE1",
    rate=50,
    start_position=7,
    length=2,
    name="Ignition Angle",
    units="deg",
    resolution_per_bit=0.1,
    data_range=(-20, 100),
)
def ignition_angle(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


# CAN ID GROUP: 0xCFFF148


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname="PE2",
    rate=50,
    start_position=1,
    length=2,
    name="Barometer",
    units="kPa",
    resolution_per_bit=0.01,
    data_range=(0, 300),
)
def barometer(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname="PE2",
    rate=50,
    start_position=3,
    length=2,
    name="MAP",
    units="kPa",
    resolution_per_bit=0.01,
    data_range=(0, 300),
)
def map_data(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)



@MessageData.deserializer(
    can_id=0xCFFF148,
    pname="PE2",
    rate=50,
    start_position=5,
    length=2,
    name="Lambda",
    units="lambda",
    resolution_per_bit=0.001,  # CHANGED FROM PE3
    data_range=(0, 10),
)
def lambda_data(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF148,
    pname="PE2",
    rate=50,
    start_position=7,
    length=1,  # should be 1 bit
    name="Pressure Type",
    data_range=(0, 255),
)
def pressure_type_data(data: bytes) -> pressure_type:
    return pressure_type(int.from_bytes(data, byteorder="little", signed=False))


# CAN ID GROUP: 0xCFFF248


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE3",
    rate=100,
    start_position=1,
    length=2,
    name="Analog Input #1",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_1(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE3",
    rate=100,
    start_position=3,
    length=2,
    name="Analog Input #2",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_2(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE3",
    rate=100,
    start_position=5,
    length=2,
    name="Analog Input #3",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_3(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE3",
    rate=100,
    start_position=7,
    length=2,
    name="Analog Input #4",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_4(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


# CAN ID GROUP: 0xCFFF348


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE4",
    rate=100,
    start_position=1,
    length=2,
    name="Analog Input #5",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_5(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE4",
    rate=100,
    start_position=3,
    length=2,
    name="Analog Input #6",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_6(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE4",
    rate=100,
    start_position=5,
    length=2,
    name="Analog Input #7",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_7(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF248,
    pname="PE4",
    rate=100,
    start_position=7,
    length=2,
    name="Analog Input #8",
    units="volts",
    resolution_per_bit=0.001,
    data_range=(0, 5),
)
def analog_input_8(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


# CAN ID GROUP: 0xCFFF448


@MessageData.deserializer(
    can_id=0xCFFF448,
    pname="PE5",
    rate=100,
    start_position=1,
    length=2,
    name="Frequency 1",
    units="Hz",
    resolution_per_bit=0.2,
    data_range=(0, 6000),
)
def frequency_1(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF448,
    pname="PE5",
    rate=100,
    start_position=3,
    length=2,
    name="Frequency 2",
    units="Hz",
    resolution_per_bit=0.2,
    data_range=(0, 6000),
)
def frequency_2(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF448,
    pname="PE5",
    rate=100,
    start_position=5,
    length=2,
    name="Frequency 3",
    units="Hz",
    resolution_per_bit=0.2,
    data_range=(0, 6000),
)
def frequency_3(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF448,
    pname="PE5",
    rate=100,
    start_position=7,
    length=2,
    name="Frequency 4",
    units="Hz",
    resolution_per_bit=0.2,
    data_range=(0, 6000),
)
def frequency_4(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


# CAN ID GROUP: 0xCFFF548


@MessageData.deserializer(
    can_id=0xCFFF548,
    pname="PE6",
    rate=1000,
    start_position=1,
    length=2,
    name="Battery Volt",
    units="volts",
    resolution_per_bit=0.01,
    data_range=(0, 22),
)
def battery_volt(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF548,
    pname="PE6",
    rate=1000,
    start_position=3,
    length=2,
    name="Air Temp",
    units="C or F",
    resolution_per_bit=0.1,
    data_range=(-1000, 1000),
)
def air_temp(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF548,
    pname="PE6",
    rate=1000,
    start_position=5,
    length=2,
    name="Coolant Temp",
    units="C or F",
    resolution_per_bit=0.1,
    data_range=(-1000, 1000),
)
def coolant_temp(data: bytes) -> int:
    return int.from_bytes(data, byteorder="little", signed=True)


@MessageData.deserializer(
    can_id=0xCFFF548,
    pname="PE6",
    rate=1000,
    start_position=7,
    length=1,
    name="Temp Type",
    data_range=(0, 255),
)
def temp_type_fn(data: bytes) -> temp_type:
    return temp_type(int.from_bytes(data, byteorder="little", signed=False))
