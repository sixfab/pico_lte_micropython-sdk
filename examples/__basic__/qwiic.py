"""

Example code for SparkFun TMP102 Qwiic digital temperature sensor.

"""

import machine
import time

# Establishing the I2C connection. '0' corresponds to the I2C driver.
# The 'SDA' and 'SCL' parameters respectively specify the SDA and SCL pins.
# The 'freq' parameter determines the I2C communication speed.

i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12), freq=100000)
tmp102_address = 0x48  # TMP102 I2C address (default set to 0x48).

# Temperature reading function
def read_temperature():
    data = i2c.readfrom(tmp102_address, 2)  # Read two bytes of data
    raw_temp = (data[0] << 8) | data[1]    # Get the raw data combined
    temperature = (raw_temp >> 4) * 0.0625 # Convert raw data to temperature value
    return temperature

while True:
    temperature = read_temperature()
    print("Temperature: {:.2f} °C".format(temperature)) # Print the temperature value
    time.sleep(1) # Slow down the loop by waiting 1 second