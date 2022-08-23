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
        "username":"[YOUR_MQTT_USERNAME]",
        "password":"[YOUR_MQTT_PASSWORD]"
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
            "[YOUR_MQTT_TOPIC/1]",
            "[YOUR_MQTT_TOPIC/2]"
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
