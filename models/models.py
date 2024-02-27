from pydantic import BaseModel


class EngineData(BaseModel):
    time: float
    rpm: int
    airTempF: float
    coolantTempF: float
    tps: float
    mapPsi: float
    batteryVolt: float
    fuelOpenTimeMs: float
    startingCompensationFuel: float
    ignitionAngleDBTDC: float
    wsFl: float
    wsRl: float
    measuredAFR1: float
    measuredAFR2: float
    targetAFR: float
    lambdaAFRLTF: float
    analog1Volts: float
    analog2Volts: float
    analog3Volts: float
    analog4Volts: float
    analog5Volts: float
    analog6Volts: float
    analog7Volts: float
    analog8Volts: float


class LabJackData(BaseModel):
    time: float
    front_left: float
    front_right: float
    rear_left: float
    rear_right: float
    x_accel: float
    y_accel: float
    z_accel: float
