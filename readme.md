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
            "host":"[YOUR_AWS_MQTT_HOST]",
            "port":"[YOUR_AWS_MQTT_PORT]",
            "pub_topic":"[YOUR_AWS_MQTT_TOPIC]",
            "sub_topics":[
                "[YOUR_MQTT_TOPIC/1]",
                "[YOUR_MQTT_TOPIC/2]"
            ]
        },

        "https":{
            "server":"[YOUR_AWS_HTTP_URL]"
        }
    }
}
```
