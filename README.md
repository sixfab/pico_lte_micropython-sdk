<p align="center">
  <img src="https://community.sixfab.com/uploads/default/original/1X/583bd28f0c2b4967aa4c275f8d388f536bc9da3d.png" height="60">
  <h1 align="center">PicoLTE SDK for MicroPython</h1>
</p>
<p align="center">
an embedded framework to make easier cellular connections
</p>
<!--
-->

<div align="center">

![version](https://img.shields.io/github/package-json/v/sixfab/picocell_python-sdk?logoColor=blue&style=flat-square) ![](https://img.shields.io/badge/license-MIT-critical?style=flat-square) ![applications](https://img.shields.io/badge/applications-6%20services-success?style=flat-square) ![stars](https://img.shields.io/github/stars/sixfab/picocell_python-sdk?style=flat-square)

</div>


Pico LTE SDK is an innovative framework that enables developers to integrate cellular communication capabilities into their embedded systems projects seamlessly. Pico LTE SDK simplifies the complexities of wireless connectivity, allowing developers to focus on their applications rather than the intricacies of cellular communication processes.

This powerful SDK empowers developers to seamlessly integrate cellular capabilities into their projects, allowing your projects to communicate over wide areas using cellular networks.

One of the standout features of Pico LTE SDK is its comprehensive compatibility with popular backend services provided by Amazon Web Services (AWS), Azure, ThingSpeak, Slack, Scriptr.io and Telegram. This integration opens up a world of possibilities for leveraging the power of cloud-based services and enables seamless communication between embedded systems and the wider Internet ecosystem.  Pico LTE SDK is a game-changer for developers seeking to integrate cellular communication capabilities into their Raspberry Pi Pico-based projects.

- **Easy Integration:** Enables seamless integration of cellular communication capabilities into embedded systems projects, specifically designed for the Sixfab Pico LTE board.
- **Minimalistic Code:** Connecting to a built-in application requires less than 40 lines of code, reducing complexity and allowing for quick and efficient development.
- **GPS Integration:** Easy-to-use GPS integration, enabling developers to incorporate location-based functionalities into their applications, leveraging cellular network-based positioning.
- **Custom Application Modules:** With the Pico LTE SDK, developers have the flexibility to create their own application modules using the SDK. This feature allows for custom functionality tailored to specific project requirements.
- **Versatile Protocols:** Pico LTE SDK simplifies the implementation of various protocols such as GPS, HTTPS, and MQTT. Developers can easily leverage these protocols for location-based services, secure web communication, and efficient machine-to-machine communication in IoT applications.

## Installation

The installation of the SDK is provided in detail and step-by-step on the ["Pico LTE SDK for MicroPython"](https://docs.sixfab.com/docs/sixfab-pico-lte-micropython-sdk) page.

- Clone the repository to your local machine or download the repository as a zip and extract it on your local machine.

- After that, upload the "[pico_lte](./pico_lte/)" folder to the root directory of your Pico LTE device. That's all.


## Usage
Using the SDK is pretty straightforward. 

Import the SDK with `from pico_lte.core import PicoLTE` line, and code your IoT project!

For more references on installation or usage, please refer to our [documentation page](https://docs.sixfab.com/docs/sixfab-pico-lte-micropython-sdk). By examining the [example codes](./examples/) provided on the platforms, you can delve into further details. You can connect various sensors to the Pico LTE, collect data on temperature, humidity, and air quality, and transmit this data over the cellular network using the Pico LTE SDK. 

Additionally, the Sixfab Community is available for any questions or suggestions you may have.

<p align="center">
  <a aria-label="Documentation on Sixfab.com" href="https://docs.sixfab.com/docs/sixfab-pico-lte-introduction" target="_blank">
    <img alt="" src="https://img.shields.io/badge/Documentation-blue.svg?style=for-the-badge">
  </a>
  <a aria-label="Community on Sixfab.com" href="https://community.sixfab.com/c/sixfab-pico-lte/36" target="_blank">
    <img alt="" src="https://img.shields.io/badge/Community-blue.svg?style=for-the-badge">
  </a>
</p>

## Configuration Files
You can use a configuration file to increase maintainability of your embedded code. This file is named as `config.json` and stores necessary connection parameters which are designed for you to easily connect to the applications. You can find example files for each application and module in [CONFIGURATIONS.md](./CONFIGURATIONS.md) page.

This file has to be in the root directory of the Pico LTE device's file system.

Please see the [Configure the Pico LTE SDK](https://docs.sixfab.com/docs/sixfab-pico-lte-micropython-sdk) page for more details.

## Contributing
All contributions are welcome. You can find the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License
Licensed under the [MIT license](https://choosealicense.com/licenses/mit/).
