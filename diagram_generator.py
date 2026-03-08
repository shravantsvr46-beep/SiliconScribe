def generate_diagram(intent):

    mcu = intent["mcu"]
    sensor = intent["sensor"]

    if sensor == "MPU6050":

        diagram = """
graph TD
    MCU[ESP32]
    SENSOR[MPU6050]

    VCC[3.3V]
    GND[GND]

    MCU -->|GPIO21 SDA| SENSOR
    MCU -->|GPIO22 SCL| SENSOR

    VCC --> SENSOR
    GND --> SENSOR
"""

    elif sensor == "IR Sensor":

        diagram = """
graph TD
    MCU[Arduino]
    SENSOR[IR Sensor]

    VCC[5V]
    GND[GND]

    MCU -->|Digital Pin| SENSOR
    VCC --> SENSOR
    GND --> SENSOR
"""

    else:

        diagram = f"""
graph TD
    USER[User Prompt]
    MCU[{mcu}]
    SENSOR[{sensor}]

    USER --> MCU
    MCU --> SENSOR
"""

    return diagram