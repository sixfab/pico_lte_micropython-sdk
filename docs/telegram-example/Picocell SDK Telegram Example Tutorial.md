# Picocell SDK Telegram Example Tutorial
## Example Description
Telegram is a globally accessible freemium, cross-platform, cloud-based instant messaging (IM) service. The service also provides optional end-to-end encrypted chats and video calling, VoIP, file sharing and several other features.
In this example, a message will be sent to the Telegram channel via Picocell using the Telegram API.

## System Requirements

### Hardware

- Picocell
- Dual LTE - GNSS Antenna
- Micro USB Cable

### Software

- Thonny IDE
- MicroPython UF2 File
- Telegram App

## Hardware Setup / Preparation

1. **Attach the LTE Antenna to the 	Quectel BG95 Module**
	Connect the GNSS port with the GPS cable and main port with the LTE cable. 
2. **Plug your board into power source**
	
#### Warning!
*For a clean install and avoiding installation errors, plug Micro USB cable into device after the software setup is complete.*



![Hardware_Setup.jpg](:/b4937e4e72c2402aaeb50e5e9c7fa096)



## Software Setup / Preparation
- Thonny is an integrated development environment (IDE) for MicroPython. It supports different ways of stepping through the code, step-by-step expression evaluation. Thonny IDE comes with Python so you can start coding quickly without dealing with tool setups. 


1. **Download Thonny IDE from it's [website](https://thonny.org).**
	- In Thonny, follow Tools > Options > Interpreter. Select MicroPython (Raspberry Pi Pico) in the list as an Interpreter. 

	![Software_Setup1.png](:/6c731a367d6f4b01b726bf17a8a3920d)


2. **Download the necessary UF2 file for Pico board from this [link](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython).**
	
	- Then go ahead and:
		- Push and hold the BOOTSEL button and plug your Pico into the USB port of your computer. Release the BOOTSEL button after your Pico is connected.
	
		![Software_Setup2.png](:/7a7549cef17241b9bf2d66c52655a858)

		- It will be mounted as a Mass Storage Device Called RPI-RP2.
		- Drag and drop the downloaded UF2 file onto the RPI-RP2 volume.
3. **Download the repo from GitHub**
- Save the core file in the repo to your Raspberry Pi Pico.
- Open the downloaded file in Thonny IDE and upload it into Raspberry Pi Pico using "Upload to /".

4. **Telegram Bot Configuration**
- Search "BotFather" in Telegram's search bar.


![Software_Setup3.png](:/d4dcfed7a8934e44bb4a5c352f5badf3)


-  Start conversation with BotFather. Type "**/start**" to see all available commands.
-  Use "**/newbot**" command to create a new bot in Telegram.


![Software_Setup4.png](:/2fb1b518ffb54d17a570e8aa8f5f44b2)

-  After creating a new bot, continue with typing your bot's name into conversation.
-  Give a username for your bot. (**Warning: Bot's "name" and "username" are different. You will use the "username" in the next steps.**)
- You will given a token automatically for accessing HTTP API. (Your token will look something like this: "**1234567890:XXX9WhkY694zP856M4xNLcr9pXX-xxxxxxx**")
***Warning: Keep your token secure and store it safely!***

5. **Telegram Setup**
- Open Telegram, create a new group or select a group to add the bot.
- Add your bot as a new member.
- Type "/my_id @YOUR_BOT_ID". After this step, your web URL is ready to use. It'll look something like this: *"https://api.telegram.org/bot**YOUR_ACCESS_TOKEN**/getUpdates"*
- Copy this URL to your browser and refresh your page.
- "getUpdates" endpoint gives all the information that you need.
- Type "/my_id @YOUR_BOT_ID" **again**. Refresh your page.

6. **URL Configuration**
- The required parameters are marked in the image below:


![Software_Setup5.png](:/f793c87918c24832963dd6ba8e328772)



7. **Base URL Setup**
- Your base URL should look like this:
*(https://api.telegram.org/bot**YOUR_ACCESS_TOKEN**/sendMessage?chat_id=**YOUR_CHAT_ID**&text=”**TEST_MESSAGE!**”)*

## Test

- Open Thonny IDE.
- Replace marked variables with your own values.

![Test1.png](:/1f85ac6805b842a5b6d34e384b64395c)

- After all this stages, run the example code. The output you get in the code should look like this: 
```
b'AT+QFLST="ufs:/security/*"\r'
Certificates found in modem.
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
PDP Test:  {'response': 'AT+CGACT?\r\r\n+CGACT: 1,1\r\n\r\nOK\r\n', 'status': 0}
b'AT+QHTTPCFG="sslctxid",2\r'
Set HTTP SSL Context {'response': 'AT+QHTTPCFG="sslctxid",2\r\r\nOK\r\n', 'status': 0}
b'AT+QHTTPURL=159,5\r'
b'https://api.telegram.org/botYOUR_ACCESS_TOKEN/sendMessage?chat_id=YOUR_CHAT_ID&text=Test message from Picocell Telegram API example!'
HTTP URL:  {'response': 'AT+QHTTPURL=159,5\r\r\nCONNECT\r\n', 'status': 0}
b'AT+QHTTPGET=60\r'
HTTP GET:  {'response': 'AT+QHTTPGET=60\r\r\nOK\r\n', 'status': 0}
b'AT+QHTTPREAD=60\r'
HTTP READ:  {'response': 'AT+QHTTPREAD=60\r\r\n+CME ERROR: 703\r\n', 'status': 1}
```

- If the process is successful, a message will be sent to the channel as in the photo:



![Test2.png](:/b64a2c845c844f88bfc67fe86699beee)



## Example Code Examination

- At the beginning of the code, functions of modem controls and settings are performed. 
```
modem = Modem(config)
atcom = ATCom()
```

- At this part, TCP/IP configuration and PDP activation are made.

```
# TCP/IP
print("TCPIP Context Configuration: ", modem.set_modem_http_context_id())
print("PDP Deactivation: ", modem.deactivate_pdp_context())
print("PDP Activatation: ", modem.activate_pdp_context())
print("PDP Test: ", atcom.send_at_comm("AT+CGACT?","OK"))
```

- In final, this code includes HTTP configuration and performs the HTTP GET request.

```
# HTTP
print("Set HTTP SSL Context", modem.set_modem_http_ssl_context_id(2))
print("HTTP URL: ", modem.set_modem_http_server_url(url=publish_url))
time.sleep(6)
print("HTTP GET: ", modem.http_get_request())
time.sleep(6)
print("HTTP READ: ", modem.http_read_response())
```

## Troubleshooting

- If there is a problem occurs while getting updated parameter informations *(see. Step 6)*, reload your browser page after sending "/my_id @YOUR_BOT_ID". You will see the updated JSON information there.


