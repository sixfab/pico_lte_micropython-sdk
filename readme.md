# Picocell Micropython SDK

# Configuration
Create `config.json` file on the root path of the Picocell.

## Configurable Parameters and their related methods
> These are used as default value while their related methods called and didn't pass an argument to these.

### For http module

```config.json
{
    "https":{
        "server":"[HTTP_SERVER]",
        "username":"[YOUR_HTTP_USERNAME]",
        "password":"[YOUR_HTTP_PASSWORD]"
    },
}
```

### For mqtt module
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

 ### For AWS app module
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

 ### For GCloud app module
```config.json
{
    "gcloud":{
        "project_id": "[YOUR_GCLOUDIOT_PROJECT_ID]",
        "region": "[YOUR_GCLOUDIOT_REGION]",
        "registry_id": "[YOUR_GCLOUDIOT_REGISTRY_ID]",
        "device_id": "[YOUR_GCLOUDIOT_DEVICE_ID]",
        "jwt": "[YOUR_JSON_WEB_TOKEN_FOR_DEVICE]",
        "mqtts": {
            "pub_topic": [YOUR_MQTT_TOPIC],
            "sub_topics": [
                "[YOUR_MQTT_TOPIC/1]",
                "[YOUR_MQTT_TOPIC/2]"
            ] 
        }
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
            "password": "[DEVICE_MQTT_PASSWORD]"
        }
    }
}
```