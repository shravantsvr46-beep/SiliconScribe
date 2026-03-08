def get_template(mcu):

    mcu = mcu.lower()

    if "esp32" in mcu or "arduino" in mcu:
        return """
Framework: Arduino

Structure:

#include <Arduino.h>

void setup() {

}

void loop() {

}
"""

    elif "stm32" in mcu:
        return """
Framework: STM32 HAL

#include "stm32f4xx_hal.h"

void SystemClock_Config(void);

int main(void)
{
    HAL_Init();
    SystemClock_Config();

    while (1)
    {

    }
}
"""

    else:
        return "Generic embedded C firmware."