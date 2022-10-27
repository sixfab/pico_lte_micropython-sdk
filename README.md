<p align="center">
  <img src="https://community.sixfab.com/uploads/default/original/1X/583bd28f0c2b4967aa4c275f8d388f536bc9da3d.png" height="60">
  <h1 align="center">picocell SDK for MicroPython</h1>
</p>
<p align="center">
an embedded framework to make easier cellular connections
</p>
<!--
-->

<div align="center">

![version: v0.2.0](https://img.shields.io/badge/version-v0.2.0-blue?style=flat-square) ![](https://img.shields.io/badge/license-MIT-critical?style=flat-square) ![applications: 6 services](https://img.shields.io/badge/applications-6%20services-success?style=flat-square) ![Stars count in GitHub](https://img.shields.io/github/stars/sixfab/picocell_python-sdk?style=flat-square)

</div>

## Description
picocell SDK is a framework that you can use in your embedded systems projects and **takes care of cellular communication** processes for you. It provides built-in application support for popular back-end services such as Amazon Web Services, Azure, ThingSpeak, Slack, and Telegram.

* Less than 40 lines when making a connection to a built-in application.
* Support for SSL/TLS certification and their secure storage.
* Easy-to-use GPS, HTTPS and MQTTS interfaces.
* Ultra-low power mode for better battery life.
* Chance to create your own application module with state machines.

## Installation
1. Go to the **Releases** section on the sidebar of this repository and download the most recent version to your computer (or download it using [this link](/sixfab/picocell_python-sdk/releases/latest/download/picocell.uf2)).
2. After downloading is finished, plug in the _picocell_ to your computer, and drag and drop the UF2 file into the _picocell_'s file system. Since the MicroPython is included in the released UF2 file, there will be no additional step to install MicroPython separately.
3. Your picocell device will be removed and re-inserted into your computer. That's all, it is ready to use!

## Usage
Using the framework is pretty straightforward. A `main.py` file is needed to run in a MicroPython environment, therefore, please create a `main.py` script in your picocell's file system. Import the framework with `from core.modem import Modem` line, and code your embedded project!

**Note**: It is a must to have a tool to upload your `main.py` file or any example from our repository to your picocell device. [Thonny IDE](https://thonny.org/) is a very common tool that has an easy GUI to perform this kind of operation. For a more compact and smaller size tool, we can recommend [Adafruit's Ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) to you.

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

This file has to be in the root directory of the picocell device's file system.



## Contributing
All contributions are welcome. You can find the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

## License
Licensed under the [MIT license](https://choosealicense.com/licenses/mit/).