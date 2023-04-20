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

## Description
PicoLTE SDK is a framework that you can use in your embedded systems projects and **takes care of cellular communication** processes for you. It provides built-in application support for popular back-end services such as Amazon Web Services, Azure, ThingSpeak, Slack, and Telegram.

* Less than 40 lines when making a connection to a built-in application.
* Support for SSL/TLS certification and their secure storage.
* Easy-to-use GPS, HTTPS and MQTTS interfaces.
* Chance to create your own application module with state machines.

## Installation
You can install the framework by cloning the repository to your local machine. You can also download the repository as a zip file and extract it to your local machine. After that, you can upload the `pico_lte` folder to your PicoLTE device's file system.

## Usage
Using the framework is pretty straightforward. A `main.py` file is needed to run in a MicroPython environment, therefore, please create a `main.py` script in your PicoLTE's file system. Import the framework with `from pico_lte.core import PicoLTE` line, and code your embedded project!

**Note**: It is a must to have a tool to upload your `main.py` file or any example from our repository to your PicoLTE device. [Thonny IDE](https://thonny.org/) is a very common tool that has an easy GUI to perform this kind of operation. For a more compact and smaller size tool, we can recommend [Adafruit's Ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) to you.

For further reference about installing or usage, please refer to our documentation page. Also, Sixfab Community Portal is available for your questions and recommendations.

<p align="center">
  <a aria-label="Documentation on Sixfab.com" href="https://docs.sixfab.com/" target="_blank">
    <img alt="" src="https://img.shields.io/badge/Documentation-blue.svg?style=for-the-badge">
  </a>
  <a aria-label="Community on Sixfab.com" href="https://community.sixfab.com/" target="_blank">
    <img alt="" src="https://img.shields.io/badge/Community-blue.svg?style=for-the-badge">
  </a>
</p>

## Configuration Files
You can use a configuration file to increase maintainability of your embedded code. This file is named as `config.json` and stores necessary connection parameters which are designed for you to easily connect to the applications. You can find example files for each application and module in [CONFIGURATIONS.md](./CONFIGURATIONS.md) page.

This file has to be in the root directory of the PicoLTE device's file system.

## Contributing
All contributions are welcome. You can find the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License
Licensed under the [MIT license](https://choosealicense.com/licenses/mit/).