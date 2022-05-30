# Clintosaurous Core Environment

Base core environment for Clintosaurous tools. It has shared modules, scripts,
and default configuration information.

It is built on shell, bash, and Python scripts.

## Table Of Contents

-   [System Requirements](#system-requirements)
    -   [Hardware](#hardware)
    -   [Operating System](#operating-system)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)

## System Requirements

### Hardware

-   Physical or virtual. Virtual is recommended. Resource utilization is low.
-   2 x Processors
-   4GB RAM (8GB RAM if running on Ubuntu desktop version.)
-   16GB Hard Drive

### Operating System

Only Ubuntu 20.04 and 22.04 are tested and supported.

## Prerequisites

1.  Ubuntu 20.04 or 22.04 server with root/sudo access.
    -   It should be dedicated to Clintosaurous tools as the tools run things
        like Apache as the Clintosaurous user.
    -   It can be Ubuntu server or desktop.
2.  cURL or Git client installed.
3.  Firewall access via HTTPS to GitHub.
4.  Firewall access for Python PIP packages.

## Installation

The installation script can be ran at any time. It will not overwrite existing
configuration or environment files. Just run it from the
`/opt/clintosaurous/core` directory.

You can install this in a couple of different ways. I suggest you use the
first method.

See `install.sh` documentation for more details on the installation process.

-   If you download the `install.sh` script and run it, the script will
    perform all the steps needed to have a base Clintosaurous core
    environment.

        curl -s https://github.com/clintosaurous/core/main/install.sh | sudo /bin/sh

-   Or, download the repository and run the installation.

        sudo mkdir /opt/clintosaurous
        sudo git clone https://github.com/clintosaurous/core.git /opt/clintosaurous/core
        sudo /opt/clintosaurous/core/install.sh

Login as the Clintosaurous user. Admins of the tools should be added to the
Clintosaurous group. It will have read-write access.

    adduser <admin-user> clintosaurous
