"""

Example code for control USER LED brightness with PWM.

"""

import machine
import utime

led = machine.Pin(22, machine.Pin.OUT)  # Set up a pin to control the LED.
pwm_led = machine.PWM(led)  # Initialize PWM (Pulse Width Modulation) for the LED.

while True:
    for duty_cycle in range(0, 65535, 1024):  # Increase LED brightness.
        pwm_led.duty_u16(duty_cycle)  # Set the LED brightness level.
        utime.sleep(0.01)  # Pause to observe the change.
    for duty_cycle in range(64511, 0, -1024):  # Decrease LED brightness.
        pwm_led.duty_u16(duty_cycle)  # Set the LED brightness level.
        utime.sleep(0.01)  # Pause to observe the change.