MCU_LIST = [
    "esp32",
    "esp8266",
    "arduino",
    "stm32",
    "raspberry pi pico",
    "pico",
    "atmega328"
]

SENSOR_LIST = [
    "mpu6050",
    "bmp280",
    "dht11",
    "dht22",
    "ultrasonic",
    "ir sensor",
    "gps",
    "oled",
    "lcd",
    "motor",
    "servo",
    "relay"
]


def parse_prompt(prompt):

    prompt_lower = prompt.lower()

    detected_mcu = "Generic MCU"
    detected_sensor = "Unknown"

    for mcu in MCU_LIST:
        if mcu in prompt_lower:
            detected_mcu = mcu.upper()
            break

    for sensor in SENSOR_LIST:
        if sensor in prompt_lower:
            detected_sensor = sensor.upper()
            break

    intent = {
        "mcu": detected_mcu,
        "sensor": detected_sensor,
        "raw_prompt": prompt
    }

    return intent


def format_intent(intent):

    return f"""
### 🔍 Parsed Hardware

| Component | Detected |
|----------|-----------|
| MCU | {intent['mcu']} |
| Peripheral | {intent['sensor']} |
"""