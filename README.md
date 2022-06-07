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
-   [Apache Installation](#apache_installation)

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
3.  lsb-release apt package installed.
4.  Firewall access via HTTPS to GitHub.
5.  Firewall access for Python PIP packages.

## Installation

The installation script can be ran at any time. It will not overwrite existing
configuration or environment files. Just run it from the
`/opt/clintosaurous/core` directory.

You can install this in a couple of different ways. I suggest you use the
first method.

See `install.sh` documentation for more details on the installation process.
Run `install.sh` with `-h` or `--help` for CLI options.

-   Direct download and run the `install.sh` script.

        curl -s https://raw.githubusercontent.com/clintosaurous/core/main/install.sh | sudo /bin/sh

-   Download `install.sh` and run it manually. This is useful if you are not
    running the default configuration. You can specify alternate information
    via CLI options. Run script with `-h` or `--help` for CLI options.

        curl -o /tmp/clintosaurous-core-install.sh https://raw.githubusercontent.com/clintosaurous/core/main/install.sh
        chmod +x /tmp/clintosaurous-core-install.sh
        sudo /tmp/clintosaurous-core-install.sh

-   Or, download the repository and run the installation.

        sudo mkdir /opt/clintosaurous
        sudo git clone https://github.com/clintosaurous/core.git /opt/clintosaurous/core
        sudo /opt/clintosaurous/core/install.sh

Login as the Clintosaurous user. Admins of the tools should be added to the
Clintosaurous group. It will have read-write access.

    adduser <admin-user> clintosaurous

## Apache Setup

Clintosaurous core environment is required to be installed before Apache
is setup. Apache setup must be performed as root.

The installation script can be ran at any time. It will not overwrite existing
configuration or environment files. Just run it from the
`/opt/clintosaurous/core` directory.

See `apache-setup.sh` documentation for more details on the installation
process. Run `apache-setup.sh` with `-h` or `--help` for CLI options.

    sudo /opt/clintosaurous/core/apache-setup.sh

NOTE: If there are firewalls in use, ensure port 443 is allowed to the server.

Default SSL key and certificate are installed. If you plan to use an alternate
SSL key and certificate, you can specify the path with CLI options or replace
the default files with your keys.
