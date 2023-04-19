"""
Example code for publising data to Azure IoT Hub Device twin by using MQTT.

Example Configuration
---------------------
Create a config.json file in the root directory of the picocell device.
config.json file must include the following parameters for this example:

config.json
{
    "azure":{
        "hub_name": "[YOUR_AZURE_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]",
        "mqtts": {
            "host": "[YOUR_AZURE_ENDPOINT]",
            "port": 8883,
            "pub_topic": "$iothub/twin/PATCH/properties/reported/?$rid=1"
            "username": "[YOUR_HUB_NAME].azure-devices.net/[YOUR_DEVICE_ID]/?api-version=2021-04-12",
            "client_id": "[YOUR_DEVICE_ID]"
        }
    }
}

Note that "mqtts" attribute is optional. To connect your IoT Hub, "hub_name" and
"device_id" is the only ones needed.
"""
import json
from pico_lte.core import PicoLTE
from pico_lte.common import debug

picoLTE = PicoLTE()

payload_json = {"App": "Azure MQTT Example"}

debug.info("Publishing data to Azure IoT Hub...")
payload = json.dumps(payload_json)
result = picoLTE.azure.publish_message(payload)
debug.info("Result", result)
