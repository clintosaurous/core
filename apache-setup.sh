#!/bin/bash

# Performs the initial Apache installation and setup of the Clintosaurous
# tools.
#
# Version: 1.0.0
# Last Updated: 2022-06-08
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-06-08)
#
# Note: See repository commit logs for change details.
#
# This can be reran at any time to validate environment is setup. Run with
# option -h or --help for run time information.
#
# The script will exit on error. It does not attempt to revert any changes
# that have already been made!
#
# Installation flow:
#
#   1.  Parse configuration file to get Clintosaurous username and group.
#   2.  Ensure the script is running on a supported OS. This check can be
#       suppressed with CLI options.
#   3.  Ensure the script is being ran as root user.
#   4.  apt update and upgrade. This can be suppressed with CLI options.
#   5.  Install required aptitude packages. This can be suppressed with CLI
#       options.
#   6.  Update Clintosaurous core environment repository. This can be
#       suppressed with CLI options.
#   7.  Create default Apache configuration file if needed.
#   9.  Add default SSL certificate and key files if needed.
#   10. Enable Clintosaurous Apache site if needed.
#   11. Create Clintosaurous user Apache account.
#   12. Add default web index page configuration if needed.
#   13. Restart Apache with updated configuration.


# Environment setup.
echo "#### Setting initial environment ####"
APTUPDATE=1
IGNOREOS=0
REPOUPDATE=1

USERHOME=/opt/clintosaurous
COREHOME=$USERHOME/core
ETCDIR=/etc/clintosaurous
CORECONF=$ETCDIR/clintosaurous.yaml
KEYFILE=/etc/apache2/default-www.key
CERTFILE=/etc/apache2/default-www.pem

. $COREHOME/lib/sh/general.sh


# Read default username and password from core configuration file.
log_msg "Parsing core configuration file for default username and password"
CONFUSER=`python3 -c "
import yaml
with open('$CORECONF', newline='') as y:
    conf = yaml.safe_load(y)
try:
    username = conf['user']['name']
    group = conf['user']['group']
    print(f'{username} {group}')
except KeyError:
    True
"`
if [ $? -ne 0 ]; then
    log_msg "Error parsing configuration file $CORECONF" >&2
    exit 1
fi

for VALUE in $CONFUSER
do
    if [ -z "$CLINTUSER" ]; then CLINTUSER=$VALUE
    else CLINTGROUP=$VALUE ; fi
done
if [ -z "$CLINTUSER" ] || [ -z "$CLINTGROUP" ]; then
    log_msg "Parsing username or user group name from $CORECONF" >&2
    exit 1
fi


# Help/usage information.
usage ()
{
    echo "
Clintosaurous Apache environment installation.

This can be reran at any time to validate environment is setup.

sudo `basename $0` [-h | --help] \\
    [ -A | --no-apt-update \\
    [ -R | --no-repo-update \\
    [ -S | --server-name \\
    [ -a | --server-admin \\
    [ -k | --ssl-key /key/file/path.key \\
    [ -c | --ssl-cert /cert/file/path.pem \\
    [ -I | --ignore-os

    -h | --help
        Display this help message.
    -A | --no-apt-update
        Skip updating the aptitude repository and installing updates, and skip
        trying to install required software
    -R | --no-repo-update
        Skip performing a git pull to update the existing repository.
    -S | --server-name
        FQDN of Apache server.
    -a | --server-admin
        Email address of the server administratory.
    -k | --ssl-key
        Alternate path to HTTPS SSL key file. Default: $KEYFILE
    -c | --ssl-cert
        Alternate path to HTTPS SSL certificate file. Default: $CERTFILE
    -I | --ignore-os
        Suppress checking OS and OS version. Although checks are suppressed,
        the command set only supports Debian based hosts.
"
    exit
}


# Process CLI options.
while [ -n "$1" ]
do
    case "$1" in
        "-h") usage ;;
        "--help") usage ;;
        "-A") APTUPDATE=0 ;;
        "--no-apt-update") APTUPDATE=0 ;;
        "-R") REPOUPDATE=0 ;;
        "--no-repo-update") REPOUPDATE=0 ;;
        "-S") shift ; SERVERNAME=$1 ;;
        "--server-name") shift ; SERVERNAME=$1 ;;
        "-a") shift ; SERVERADMIN=$1 ;;
        "--server-admin") shift ; SERVERADMIN=$1 ;;
        "-k") shift; KEYFILE=$1 ;;
        "--ssl-key") shift; KEYFILE=$1 ;;
        "-c") shift; CERTFILE=$1 ;;
        "--ssl-cert") shift; CERTFILE=$1 ;;
        "-I") IGNOREOS=1 ;;
        "--ignore-os") IGNOREOS=1 ;;
        *) echo "Unknown CLI option $1" ; echo ; usage ;;
    esac
    shift
done


# Verify running on supported OS and running as root.
if [ $IGNOREOS -ne 0 ]; then check_valid_os ; fi
check_login_user root

# Header.
log_msg "#### Clintosaurous Apache initial setup starting ####"


# Install required packages.
if [ $APTUPDATE -ne 0 ]; then
    log_msg "Installing required aptitude packages"

    log_msg "Updating system"
    apt update -q && apt upgrade -q -y 2>&1 | log_stdin
    if [ $? -ne 0 ]; then
        log_msg "Error updating aptitude packages" >&2
        exit 1
    fi

    log_msg "Installing required aptitude packages"
    apt install -q -y apache2 apache2-suexec-pristine 2>&1 | log_stdin
    if [ $? -ne 0 ]; then
        log_msg "Error installing required aptitude packages" >&2
        exit 1
    fi

    # Create httpd sym link for the apache2 server.
    if [ ! -e /lib/systemd/system/httpd.service ]; then
        ln -s /lib/systemd/system/apache2.service \
            /lib/systemd/system/httpd.service
        systemctl daemon-reload
    fi

    # Enable Apache modules.
    log_msg "Enabling apache2 modules"
    a2enmod auth_form cgi request rewrite \
        session session_cookie ssl socache_shmcb 2>&1 | log_stdin
    if [ $? -ne 0 ]; then
        log_msg "Error enabling Apache required modules" >&2
        exit 1
    fi

    log_msg "Enabling Apache"
    systemctl enable apache2 2>&1 | log_stdin
    if [ $? -ne 0 ]; then
        log_msg "Error enabling Apache" >&2
        exit 1
    fi
fi


# Ensure repository is cloned and up to date.
if [ $REPOUPDATE -ne 0 ]; then
    if [ -e $COREHOME ]; then
        if [ -e $COREHOME/LICENSE ]; then
            log_msg "Clintosaurous core directory directory exists"
            # Must be ran as Clintosaurous user.
            su - -c "cd $COREHOME && git pull" $CLINTUSER 2>&1 | log_stdin
            if [ $? -ne 0 ]; then
                log_msg "Error updating Clintosaurous core repository" >&2
                exit 1
            fi
        else
            MSG="Clintosaurous core directory exists, but is not from the"
            MST="$MSG GitHub repository!"
            log_msg "$MSG" >&2
            exit 1
        fi
    else
        MSG="Clintosaurous core envirnoment must be installed and setup."
        MSG="$MSG Run the core installation (install.sh) and then retry."
        log_msg "$MSG" 1>&2
        exit 1
    fi
fi


# Ensure configuration file exists. If not, add it and enable it.
A2CONF=/etc/apache2/sites-available/clintosaurous.conf
if [ ! -e $A2CONF ]; then
    # Get server name for configuration file.
    if [ -z "$SERVERNAME" ]; then
        echo -n "Enter server FQDN: " ; read SERVERNAME
    fi
    # Get site admin email for configuration file.
    if [ -z "$SERVERADMIN" ]; then
        echo -n "Enter server admin email: " ; read SERVERADMIN
    fi

    # Disable the default configuration file.
    if [ -e /etc/apache2/sites-enabled/000-default.conf ]; then
        log_msg "Disabling Apache default configuration"
        a2dissite 000-default 2>&1 | log_stdin
        if [ $? -ne 0 ]; then
            log_msg "Error diabling Apache default site" >&2
            exit 1
        fi
    fi

    log_msg "Adding default configuration file"
    cp $COREHOME/lib/defaults/apache2.conf $A2CONF 2>&1| log_stdin

    if [ -e $CERTFILE ]; then
        log_msg "Certificate exists"
    else
        log_msg "Adding default web certificate and key"
        cp /opt/clintosaurous/core/lib/defaults/default-www.key $KEYFILE \
            2>&1| log_stdin
        cp /opt/clintosaurous/core/lib/defaults/default-www.pem $CERTFILE \
            2>&1| log_stdin
        chmod 600 $KEYFILE 2>&1| log_stdin
        chown $CLINTUSER:$CLINTGROUP $KEYFILE $CERTFILE 2>&1| log_stdin
    fi

    log_msg "Setting Apache run time user"
    sed -Ei "s/APACHE_RUN_USER=.+/APACHE_RUN_USER=$CLINTUSER/" \
        /etc/apache2/envvars 2>&1| log_stdin
    log_msg "Setting Apache run time group"
    sed -Ei "s/APACHE_RUN_GROUP=.+/APACHE_RUN_GROUP=$CLINTGROUP/" \
        /etc/apache2/envvars 2>&1| log_stdin
    log_msg "Setting Apache server name"
    sed -Ei "s/<<<server-name>>>/$SERVERNAME/" $A2CONF 2>&1| log_stdin
    log_msg "Setting Apache server admin"
    sed -Ei "s/<<<server-admin>>>/$SERVERADMIN/" $A2CONF 2>&1| log_stdin
    log_msg "Setting Apache SSL key file"
    sed -Ei "s|<<<key-file>>>|$KEYFILE|" $A2CONF 2>&1| log_stdin
    log_msg "Setting Apache SSL certificate file"
    sed -Ei "s|<<<cert-file>>>|$CERTFILE|" $A2CONF 2>&1| log_stdin

    if [ ! -e /etc/apache2/sites-enabled/clintosaurous.conf ]; then
        log_msg "Enabling Clintosaurous configuration"
        a2ensite clintosaurous 2>&1| log_stdin
        if [ $? -ne 0 ]; then
            log_msg "Error enabling Apache clintosaurous site" >&2
            exit 1
        fi
    fi

fi

PASSFILE=/etc/apache2/htpasswd
if [ ! -e $PASSFILE ]; then
    log_msg "Setting up $CLINTUSER user for web access"

    # Password would not set properly from a script on Ubuntu 20.04. Must be
    # manually created from the command line with the password as a parameter.
    BADOS=0
    if [ $IGNOREOS -eq 0 ]; then
        . /etc/lsb-release
        if [ "$DISTRIB_RELEASE" = "20.04" ]; then
            echo
            echo -n "Apache 2 user must be created manually! As of " >&2
            echo -n "2022-06-08, there is a bug in Apache htpasswd that " >&2
            echo -n "will not allow scripted user creation. The password " >&2
            echo -n "would not be set correctly and the user cannot " >&2
            echo -n "login to the web site. The password must also be " >&2
            echo "set using a CLI argument at the command line." >&2
            echo >&2
            echo "Commands:" >&2
            echo "    sudo htpasswd -bc /etc/apache2/htpasswd $CLINTUSER <passwd>" >&2
            echo "    sudo chmod 660 $PASSFILE" >&2
            echo "    sudo chown $CLINTUSER:$CLINTGROUP $PASSFILE" >&2
            echo
            BADOS=1
        fi
    fi

    if [ $BADOS -eq 0 ]; then
        echo
        echo "Creating $CLINTUSER Apache user"
        echo "WARNING: Do not use Linux special characters in the password!"
        echo

        CLINTPASSWD=0
        PASSWDCONFIRM=1
        while [ "$CLINTPASSWD" != "$PASSWDCONFIRM" ]; do
            read -s -p "Enter $CLINTUSER web password: " CLINTPASSWD
            echo
            read -s -p "Re-enter $CLINTUSER web password: " PASSWDCONFIRM
            echo
            if [ "$CLINTPASSWD" != "$PASSWDCONFIRM" ]; then
                echo
                echo "Passwords do not match, try again."
            fi
        done

        echo "$CLINTPASSWD" | htpasswd -ci $PASSFILE $CLINTUSER
        if [ $? -ne 0 ]; then
            log_msg "Error creating Apache user $CLINTUSER" >&2
            exit 1
        fi
        chmod 660 $PASSFILE
        chown $CLINTUSER:$CLINTGROUP $PASSFILE
    fi
fi


# Validate default index configuration file exits.
if [ -e $ETCDIR/www-index.yaml ]; then
    log_msg "Default index page configuration exists"
else
    log_msg "Adding index page default configuration"
    cp $COREHOME/lib/defaults/www-index.yaml $ETCDIR/ 2>&1| log_stdin
    chown -R $CLINTUSER:$CLINTGROUP $ETCDIR/ 2>&1| log_stdin
    chmod g+w,o= $ETCDIR/www-index.yaml 2>&1| log_stdin
fi


APACHERELOAD=1
if [ ! -e "$KEYFILE" ]; then
    MSG="SSL key file $KEYFILE does not exist. Update Apache configuration"
    MSG="$MSG with correct key location, or place key at $KEYFILE."
    log_msg "$MSG"
    APACHERELOAD=0
fi
if [ ! -e "$CERTFILE" ]; then
    MSG="SSL certificate file $CERTFILE does not exist. Update Apache"
    MSG="$MSG configuration with correct certificate location, or place"
    MSG="$MSG key at $KEYFILE."
    log_msg "$MSG"
    APACHERELOAD=0
fi

if [ $APACHERELOAD -ne 0 ]; then
    log_msg "Restarting Apache service"
    systemctl restart apache2 2>&1 | log_stdin
    if [ $? -ne 0 ]; then
        MSG="Error enabling Apache clintosaurous site. Check Apache service"
        MSG="$MSG status or error log for more details"
        log_msg "$MSG" >&2
        exit 1
    fi
fi


log_msg "#### Clintosaurous Apache setup complete ####"
