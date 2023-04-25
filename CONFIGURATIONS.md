# Configuration Files
Each application module designed to work with configuration files for easier manipulation to server-side changes. A configuration file is named as `config.json` and stores necessary connection parameters which are designed for you to easily connect to the applications.

In this file, you can find example configuration files for each application module and their mandatory and optional parameters. This file must be placed on the root directory of PicoLTE module.

## Table of Contents
1. [Amazon Web Services IoT Core](#amazon-web-services-iot-core-configurations)
2. [Microsoft Azure IoT Hub](#microsoft-azure-iot-hub-configurations)
3. [Slack](#slack-configurations)
4. [Telegram](#telegram-configurations)
5. [ThingSpeak™](#thingspeak-configurations)
6. [Native HTTPS](#https-configurations)
7. [Native MQTTS](#mqtts-configurations)
8. [Configuration Files for Your Own Application Module](#configuration-files-for-your-own-application-module)

## Applications
In this section, we're going to give you better understanding about how to create a `config.json` file for specific application modules.

### Amazon Web Services IoT Core Configurations
You can select MQTTS or HTTPS protocol and delete the other attribute.
```json
{
    "aws": {
        "host": "[YOUR_AWSIOT_ENDPOINT]",
        "port": "[YOUR_AWSIOT_MQTT_PORT]",
        "pub_topic": "[YOUR_MQTT_TOPIC]",
        "sub_topics": [
                "[YOUR_MQTT_TOPIC/1]",
                "[YOUR_MQTT_TOPIC/2]"
        ],
    }
}
```

### Microsoft Azure IoT Hub Configurations
Within this level of configurations, you can use Azure IoT Hub directly.
```json
{
    "azure": {
        "hub_name": "[YOUR_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]"
    }
}
```
For more detailed configuration, you may want to use extra MQTTS parameters. Each attribute in MQTTS is optional.
```json
{
    "azure": {
        "hub_name": "[YOUR_IOT_HUB_NAME]",
        "device_id": "[YOUR_DEVICE_ID]",
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
}
```

### Slack Configurations
To connect Slack, only need is a WebHook URL, there is no more detailed attributes.

```json
{
    "slack":{
        "webhook_url": "[INCOMING_WEBHOOK_URL]"
    }
}
```

### Telegram Configurations
Within this level of configurations, you can use Telegram directly.
```json
{
    "telegram": {
        "token": "[YOUR_BOT_TOKEN_ID]",
        "chat_id": "[YOUR_GROUP_CHAT_ID]"
    }
}
```
In case of future server URL changes in Telegram side, you may want to add `server` attribute as shown below.
```json
{
    "telegram": {
        "server": "[TELEGRAM_BOT_API_ENDPOINT]",
        "token": "[YOUR_BOT_TOKEN_ID]",
        "chat_id": "[YOUR_GROUP_CHAT_ID]"
    }
}
```


### ThingSpeak Configurations
Within this level of configurations, you can use ThingSpeak directly. Subscription and publish operations are made directly to all channel fields.
```json
{
    "thingspeak": {
        "channel_id": "[YOUR_CHANNEL_ID]",
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",
        "pub_field": [FIELD_NO_INTEGER],
        "sub_fields": [FIELD_NO_INTEGER, FIELD_NO_INTEGER_2, ...]
    }
}
```
For better control on which fields to subscribe or publish, you may want to add extra attributes. Also, please note that host and port address can be change by its own attributes. Note that FIELD_NO_INTEGER is an integer value which is the number of the field in the channel or "+" string if all the fields are desired.
```json
{
    "thingspeak": {
        "channel_id": "[YOUR_CHANNEL_ID]",
        "host": "[THINGSPEAK_HOST_ADDRESS]",
        "port": "[THINGSPEAK_PORT_ADDRESS]",
        "client_id": "[DEVICE_MQTT_CLIENT_ID]",
        "username": "[DEVICE_MQTT_USERNAME]",
        "password": "[DEVICE_MQTT_PASSWORD]",

        // Use either sub_topics or sub_fields.
        "sub_topics": [
            ["[YOUR_MQTT_TOPIC]", [QOS]]
        ],
        "sub_fields": [FIELD_NO_INTEGER, FIELD_NO_INTEGER_2, ...],

        "pub_field": [FIELD_NO_INTEGER],
        }
    }
}
```
## Modules
Some use-cases can be implemented by using modules when there is no spesific application for that use-case. In this situtations, the developers can built their own solutions with using HTTPS and MQTTS modules.

### HTTPS Configurations
```json
{
    "https": {
        "server": "[HTTP_SERVER]",
        "username": "[YOUR_HTTP_USERNAME]",
        "password": "[YOUR_HTTP_PASSWORD]"
    }
}
```
### MQTTS Configurations
```json
{
    "mqtts": {
        "host": "[YOUR_MQTT_HOST]",
        "port": "[YOUR_MQTT_PORT]",
        "pub_topic": "[YOUR_MQTT_PUB_TOPIC]",
        "sub_topics": [
            ["[YOUR_MQTT_TOPIC/1]",[QOS]],
            ["[YOUR_MQTT_TOPIC/2]",[QOS]]
        ],
        "username": "[YOUR_MQTT_USERNAME]",
        "password": "[YOUR_MQTT_PASSWORD]"
}
```

## Configuration Files for Your Own Application Module
The most important feature that we've developed in PicoLTE SDK is the ability to create new applications for your specific services. Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) guidelines. You need to follow standarts that we used to create an application configuration parameters.

 This is the general structure of a `config.json` file:
 ```
 {
    "your_own_app": {
        [application_specific_attributes],
        // If the connection made with MQTTS:
        "mqtts": {
            "host": "",
            "port": "",
            "pub_topic": "",
            "sub_topics": [
                ["", [QOS]],
                ["", [QOS]]
            ],
            "username": "",
            "password": ""
        },
        // If the connection made with HTTPS:
        "https": {
            "server": "",
            "username": "",
            "password": ""
        }
    }
 }
 ```
 In case of redundant parameter in MQTTS or HTTPS, you can remove it from the structure.