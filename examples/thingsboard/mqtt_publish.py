"""
Example code for publish topics for ThingsBoard and
recerving data from ThingsBoard channel by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

{
    "thingsboard": {      
        "device":"[YOUR_MQTT_DEVICE]",
        "client_id":"[CLIENT_ID]",
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",
        "qos": "[QoS]",
    }
}
"""

from pico_lte.core import PicoLTE
from pico_lte.common import debug
import machine
import utime
import json

picoLte = PicoLTE()

debug.info("Publishing temperature data to ThingsBoard...")
TEMP_SENSOR_PIN = 4


def adc_to_voltage(adc_value):
    max_adc_value = 65535
    return adc_value * (3.3 / max_adc_value)


def adc_to_temperature(adc_value):
    voltage = adc_to_voltage(adc_value)
    reference_voltage = 0.706
    temperature_factor = 0.001721
    return 27 - ((voltage - reference_voltage) / temperature_factor)


while True:
    adc_value = machine.ADC(TEMP_SENSOR_PIN).read_u16()
    temperature = adc_to_temperature(adc_value)
    payload = {"temperature": temperature}
    payload = json.dumps(payload)
    result = picoLte.thingsboard.publish_message(payload)
    debug.info(f"Result: {result}, Temp: {temperature:.2f}°C")
    utime.sleep(30)
