# scriptr.ip API Usage with Picocell

In this example, sending data to the scriptr.io script via a Scriptr App will be performed.

## Description

Scriptr.io is a very powerful cloud service for running server-side code. At scriptr.io, use scripts to create custom backend APIs for Internet of Things (IoT) and other projects. Scriptr.io helps you be productive quickly by providing an integrated web-based environment for developing, running, and debugging your code.

## System Requirements

### Hardware

- Picocell w/ Quectel BG95-M3 
- USB cable
- LTE - GNSS Dual u.FL Antenna  – 100mm

### Software

- MicroPython UF2 file

- Thonny IDE

- scriptr.io account

  

## Hardware Setup / Preparation

1. Attach the antenna to the Quectel BG95-M3

   Make sure the right antenna is connected to the right port. Connect Quectel's main port with the antenna's LTE cable, and the GNSS port with the GPS cable.

2. Plug into the power source

   Make sure your Raspberry Pi Pico is not connected to any power sources. If it is, unplug the micro USB cable and any other cables that may be powering the board. Keep pressing the BOOTSEL button while connecting the micro USB cord (which hopefully has the other end plugged into your computer). 

   You can go to the [link](https://www.raspberrypi.com/document/microcontrollers/micropython.html) to access more information about Raspberry Pi Pico and review the installation in more detail.


![](assets/Hardware_Setup.jpeg)

## Software Setup / Preparation ##

1. Run MicroPython

   After connecting Picocell to your computer, it will be mounted as a Mass Storage Device named RPI-RP2. Drag and drop the MicroPython UF2 file (Download from the [link](https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2)) onto the RPI-RP2 volume. Your Pico will reboot. You are now running MicroPython. 

   To access and review the Raspberry Pi Pico Python SDK in more detail, go to the [link](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf).

2. Install and run the Thony IDE

   The latest release of Thonny can be downloaded from the [link](https://thonny.org/).

3. Download Github Repository

   Download the repo from the [link](https://github.com/sixfab/picocell_python-sdk) and save the core file in the repo to Raspberry Pi Pico. To do this, first, open the downloaded file in Thonny IDE under *This Computer* and right-click on the core file, and upload it into Pico with "Upload to /".

4. Login to scriptr.io

   Login to your scriptr.io account from [the login page](https://www.scriptr.io/login), if you do not have an account, create a new account from [the registration page](https://www.scriptr.io/register).

   > **Warning**
   >
   > The verification email may be in the spam folder of your mailbox, please check this folder too.

5. Test your workspace

   When you log in to your account, you can send your first request and test the workspace by running the "Hello Device" script, which is attached by default, with the "run" command.

![](assets/Software_Setup_1.png)

​	

​	As seen in the example, communication with the platform is done with a simple POST request. 

```bash
curl -X POST  -H 'Authorization: bearer QzAyOUIyNzE5RTpzY3JpcHRyOjg3MkQxRDRBRkYwOTUyREQ3MDBFMDA5QzI2NzQxQTQ4' 'https://api.scriptrapps.io/HelloDevice'
```

​	How to make this request with Picocell is explained in the following parts of the article.



6. Demo with Creatr

   With the Creatr guide, you will be able to connect a device to scriptr.io, select a use case then launch a demo app that will process and visualize your device data. In this way, you will perform the first step of how to send data to a script with Picocell.

   Go to the [Creatr page](https://www.scriptr.io/creatr) to start the demo. Continue with the *GET STARTED* button.

   Continue with Other Device as we will be sending data via Picocell.

   

![Selecting device](assets/Software_Setup_2.png)

7. Create your device

   Enter the name of the device to which you will send data and select the path to transmit the data. In this example, since the data will be sent with Picocell, continue with the "My device will push the data to a script" option.

​	![Device creating](assets/Software_Setup_3.png)

8. Protocol selecting and `config.json` file

   Go with HTTP as this example happens with the HTTP protocol. Here, the script is created automatically with Creatr. Save the data marked in red for the config.json file in a file and continue with the next button.

![Protocol Selecting](assets/Software_Setup_4.png)



## Test

Create the `config.json` file for the example as shown below and use the information you saved in step 8.

```
{
    "scriptr":{
        "query": "/creatr/samples/findMe***********",
        "authorization": "Qz*****************************************************"
    }
}
```

>**Warning**
>
>When creating the config.json file, don't forget to put slash (/) in front of the scriptName.



Load the `config.json` file and `core` file into Raspberry Pi Pico and write the data you want to send as JSON to the `payload_json `constant shown in the code. After doing all this, go to the code `examples/scriptr_io/send_data.py` and run the example.

![](assets/Test_1.png)



When the message is transmitted successfully, the output is as follows:

````python
INFO: Sending data to scriptr.io script...
INFO: Result: {'status': 1, 'response': ['+QHTTPPOST: 0,400'], 'interval': 0}
````



On the creatr page, the data will appear as in the picture. If you want to continue the Demo, check the next steps of the [tutorial](https://blog.scriptr.io/connecting-your-device-to-scriptr-io-using-creatr/).

![](assets/Test_2.png)



Go to the workspace to see the transmitted data and the JSON Map generated for that data.

![Creatr sample](assets/Test_3.png)

![JSON Map](assets/Test_4.png)



## Example Code Examination

In the given sample code, we first add the libraries we will use, including our Picocell SDK. In the second part of the code, we create an object called modem so that we can use the features of our Picocell SDK and send a POST request over it. Next, we create the payload_json object with the JSON we will send and perform the POST request.



## Troubleshooting

- Although data is transmitted, sometimes "timeout" is returned as output.
