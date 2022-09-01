# Picocell Micropython SDK

# Configuration
Create `config.json` file on the root path of the Picocell.

## Configurable Parameters and their related methods
> These are used as default value while their related methods called and didn't pass an argument to these.

### For HTTP module

```config.json
{
    "https":{
        "server":"[HTTP_SERVER]",
        "username":"[YOUR_HTTP_USERNAME]",
        "password":"[YOUR_HTTP_PASSWORD]"
    },
}
```

### For MQTT module
```config.json
{
    "mqtts":{
        "host":"[YOUR_MQTT_HOST]",
        "port":"[YOUR_MQTT_PORT]",
        "pub_topic":"[YOUR_MQTT_PUB_TOPIC]",
        "sub_topics":[
            ["[YOUR_MQTT_TOPIC/1]",[QOS]],
            ["[YOUR_MQTT_TOPIC/2]",[QOS]]
        ],
        "username":"[YOUR_MQTT_USERNAME]",
        "password":"[YOUR_MQTT_PASSWORD]"
}
```

 ### For Amazon Web Services app module
```config.json
{
    "aws":{
        "mqtts":{
            "host":"[YOUR_AWSIOT_ENDPOINT]",
            "port":"[YOUR_AWSIOT_MQTT_PORT]",
            "pub_topic":"[YOUR_MQTT_TOPIC]",
            "sub_topics":[
                "[YOUR_MQTT_TOPIC/1]",
                "[YOUR_MQTT_TOPIC/2]"
            ]
        },

        "https":{
            "endpoint":"[YOUR_AWS_IOT_ENDPOINT]"
            "topic":"[YOUR_DEVICE_TOPIC]"
        }
    }
}
```

 ### For Telegram app module
```config.json
{
    "telegram": {
        "token": "[YOUR_BOT_TOKEN_ID]",
        "chat_id": "[YOUR_GROUP_CHAT_ID]"
        }
}
```

### For Slack app module

```config.json
{
    "slack":{
        "webhook_url": "[INCOMING_WEBHOOK_URL]"
    }
}
```

### For ThingSpeak app module
```config.json
{
    "thingspeak": {
        "channel_id": "[YOUR_CHANNEL_ID]",
        "mqtts": {
            "client_id": "[DEVICE_MQTT_CLIENT_ID]",
            "username": "[DEVICE_MQTT_USERNAME]",
            "password": "[DEVICE_MQTT_PASSWORD]",
            "sub_topics": [
                ["[YOUR_MQTT_TOPIC]", [QOS]]
            ],
            "pub_topic": "[YOUR_MQTT_TOPIC]"
        }
    }
}
```

### For Azure IoT Hub app module:
```config.json
{
    "azure": {
        "hub_name": "[YOUR_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]"
    }
}
```