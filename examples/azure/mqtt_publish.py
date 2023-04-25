"""
Example code for publising data to Azure IoT Hub Device twin by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the PicoLTE device.
config.json file must include the following parameters for this example:

config.json
{
    "azure":{
        "hub_name": "[YOUR_AZURE_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]",
    }
}
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"App": "Azure MQTT Example"}
payload = json.dumps(payload_json)

debug.info("Publishing data to Azure IoT Hub...")
result = picoLTE.azure.publish_message(payload)
debug.info("Result", result)
