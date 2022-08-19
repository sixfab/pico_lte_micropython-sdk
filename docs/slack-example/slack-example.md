# Slack API Usage with Picocell

In this example, sending a message to the Slack channel via a Slack App with the Slack API will be performed.

## Description

Slack is a cloud-based business chat platform that links users to the data they require. Also, Slack changes how businesses communicate by uniting employees to work as a single cohesive team. The Slack API offers a user interface for retrieving information and making changes in a Slack workplace.

## System Requirements

### Hardware

- Picocell w/ Quectel BG95-M3 
- USB cable
- LTE - GNSS Dual u.FL Antenna  – 100mm

### Software

- MicroPython UF2 file

- Thonny IDE

- Slack Workspace, App, and Channel

  

## Hardware Setup / Preparation

1. Attach the antenna to the Quectel BG95-M3

   Make sure the right antenna is connected to the right port. Connect Quectel's main port with the antenna's LTE cable, and the GNSS port with the GPS cable.

2. Plug into the power source

   Make sure your Raspberry Pi Pico is not connected to any power sources. If it is, unplug the micro USB cable and any other cables that may be powering the board. Keep pressing the BOOTSEL button while connecting the micro USB cord (which hopefully has the other end plugged into your computer). 
   
   You can go to the [link](https://www.raspberrypi.com/document/microcontrollers/micropython.html) to access more information about Raspberry Pi Pico and review the installation in more detail.
   

![Hardware Setup](assets/Hardware_Setup.jpeg)

## Software Setup / Preparation ##

1. Run MicroPython

   After connecting Picocell to your computer, it will be mounted as a Mass Storage Device named RPI-RP2. Drag and drop the MicroPython UF2 file (Download from the [link](https://micropython.org/download/rp2-pico/rp2-pico-latest.uf2)) onto the RPI-RP2 volume. Your Pico will reboot. You are now running MicroPython. 

   To access and review the Raspberry Pi Pico Python SDK in more detail, go to the [link](https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf).

2. Install and run the Thony IDE

   The latest release of Thonny can be downloaded from the [link](https://thonny.org/).

3. Download Github Repository

   Download the repo from the [link](https://github.com/sixfab/picocell_python-sdk/tree/feat/slack-example/examples) and save the core file in the repo to Raspberry Pi Pico. To do this, first, open the downloaded file in Thonny IDE under *This Computer* and right-click on the core file, and upload it into Pico with "Upload to /".

4. Create a Slack Workspace

   Log in to Slack with your e-mail address from the [link][ https://slack.com/]. Then, click the “Create a New Workspace” button or continue with other workspaces you have created.

   Continue the first step of the four-step process by entering your company or team name (ex. *Sixfab*). 

   ![Workspace creating step one](assets/Software_Setup_1.png)

   In the second step, give brief information about the project that your company or team is currently working on it (ex. *PicoCell SDK Test*). 

   ![Workspace creating step 2](assets/Software_Setup_2.png)

   Complete the third step by entering their e-mail addresses to add your teammates -you can choose the "Skip for now" option to quickly pass this stage.- Workspace has been successfully created!

5. Create an App

   After creating the Workspace, the app that will send the message needs to be created. For this, go to the [link](https://api.slack.com/) in a separate tab. Click "Create an app" to create a new app for sending messages, or click “Your apps” to view and use Apps you have created before.

   If you continue by creating a new App, select the "From scratch" option. 

   <img src="assets/Software_Setup_3.png" alt="App configuration" style="zoom:60%;" />

   Then enter the name of your App (ex. *Picocell_test*) and select the workspace to work in. You can choose the workspace you created in the previous step or a workspace you created earlier.

   <img src="assets/Software_Setup_4.png" alt="App creating" style="zoom:60%;" />

6. Add Webhook Feature

   On the screen that appears for editing the app, go to Incoming Webhooks from the Features section. You need to activate this feature.

<img src="assets/Software_Setup_5.png" alt="Webhook Feature" style="zoom:60%;" />

After activation, scroll down the page and click "Add New Webhook to Workspace". Then select the channel to which the App will be added, that is, to which you want to send a message.

<img src="assets/Software_Setup_6.png" alt="App Permission and Channel Choosing" style="zoom:60%;" />

If the actions are successful, you will have obtained a Webhook URL and will also be viewing your App in the channel you added.

<img src="assets/Software_Setup_7.png" alt="Webhook URL" style="zoom:60%;" />

Your Webhook URL that'll look something like this:

```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

That URL is your new Incoming Webhook, one that's specific to a single user, and a single channel.



## Test ##

After all this build-up, just make an HTTP POST request like this:

```
POST https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
Content-type: application/json
{
	"text": "Hello, world."
}
```

A few tweaks are required to perform this request in the PicoCell SDK. First of all, create a constant named *SERVER_URL*, which contains the host and query, and edit the Webhook URL that you created in the previous steps as you can see:

```python
SERVER_DETAILS = {
    'HOST': 'https://hooks.slack.com',
    'QUERY': '/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
}
```

Next, create a constant for the message you're sending:

```python
DATA = {
  'text': 'Message from PicoCell!'
}
```

After completing all these steps, when you run the code, the message you want to send will be successfully transmitted. The output you get in the code should look like this:

```
b'AT+QFLST="ufs:/security/*"\r'
Error occured while getting certificates from modem!
b'AT\r'
COM:  {'response': 'AT\r\r\nOK\r\n', 'status': 0}
b'AT+CGDCONT=1,"IP","super"\r'
Set APN:  {'response': 'AT+CGDCONT=1,"IP","super"\r\r\nOK\r\n', 'status': 0}
b'AT+COPS?\r'
COPS:  {'response': 'AT+COPS?\r\r\n+COPS: 0,0,"Turk Telekom",0\r\n\r\nOK\r\n', 'status': 0}
b'AT+QICSGP=1,1,"super","","",1\r'
{'response': 'AT+QICSGP=1,1,"super","","",1\r\r\nOK\r\n', 'status': 0}
b'AT+QHTTPCFG="contextid",1\r'
TCPIP Context Configuration:  {'response': 'AT+QHTTPCFG="contextid",1\r\r\nOK\r\n', 'status': 0}
b'AT+QIDEACT=1\r'
PDP Deactivation:  {'response': 'AT+QIDEACT=1\r\r\nOK\r\n', 'status': 0}
b'AT+QIACT=1\r'
PDP Activatation:  {'response': 'AT+QIACT=1\r\r\nOK\r\n', 'status': 0}
b'AT+CGACT?\r'
PDP Test:  {'response': 'AT+CGACT?\r\r\n+CGACT: 1,1\r\n+CGACT: 2,0\r\n\r\nOK\r\n', 'status': 0}
b'AT+QHTTPURL=23,5\r'
b'https://hooks.slack.com'
HTTP URL:  {'response': 'AT+QHTTPURL=23,5\r\r\nCONNECT\r\n', 'status': 0}
b'AT+QHTTPCFG="requestheader",1\r'
b'AT+QHTTPPOST=213,5,60\r'
b'POST /services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX HTTP/1.1\nHost: hooks.slack.com\nCustom-Header-Name: Custom-Data\nContent-Type: application/json\nContent-Length: 35\n\n\n{"text": "Message from PicoCell!"}'
HTTP POST:  {'response': '\r\nOK\r\n', 'status': 0}
b'AT+QHTTPREAD=60\r'
HTTP READ:  {'response': '\r\n+QHTTPPOST: 0,200\r\nAT+QHTTPREAD=60\r\r\nCONNECT\r\nok\r\nOK\r\n\r\n+QHTTPREAD: 0\r\n', 'status': 0}
```



If the message is sent, it will be forwarded to the channel as shown in the image:

<img src="assets/Test.png" alt="Test" style="zoom:60%;" />



## Example Code Examination ##

At the beginning of the code, the connection controls and settings of the modem are performed. After TCP/IP configuration and PDP activation, an HTTP request is made. In this request, the URL of the address to which we will send the request is set by pulling the generated SERVER_DETAILS parameter.

```python
print("HTTP URL: ", modem.set_modem_http_server_url(url = SERVER_DETAILS["HOST"]))
```

Since a header will be sent in the request, *requestheader* activation takes place in the code line below.

```python
atcom.send_at_comm('AT+QHTTPCFG="requestheader",1')
```

Finally, the header first and then the data to be sent are sent with the POST request:

```python
print("HTTP POST: ", modem.http_post_request(data = header + data_post_json))
```



## Troubleshooting ##

If new features and scopes are added to the App to be used for sending messages, the page must be reloaded and the "Incoming Webhook" feature must be checked. A new Webhook URL may have been created, in which case it should be remembered to update the SERVER_DETAIL parameter.
