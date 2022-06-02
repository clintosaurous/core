#!/bin/sh

# Performs the initial Apache 2 installation and setup of the Clintosaurous
# tools.
#
# Version: 1.0.0
# Last Updated: 2022-05-31
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-31)
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
#   1.  Ensure the script is running on an Ubuntu 20.04 or 22.04 system. This
#       check can be suppressed with CLI options.
#   2.  Ensure the script is being ran as root user.
#   3.  apt update and upgrade. This can be suppressed with CLI options.
#   4.  Install required aptitude packages.
#   7.  Update Clintosaurous core environment repository.
#   9.  Create default Apache 2 configuration file if needed.
#   14. Install required PIP modules.


# Environment setup.
echo "#### Setting initial environment ####"
APTUPDATE=1
CLINTUSER=clintosaurous
CLINTGROUP=clintosaurous
USERHOME=/opt/clintosaurous
COREHOME=$USERHOME/core
CORECONF=/etc/clintosaurous/core.yaml
KEYFILE=/etc/apache2/default-www.key
CERTFILE=/etc/apache2/default-www.pem

# Read default username and password from core configuration file.
echo "Parsing core configuration file for default username and password"
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
if [ -n "$CONFUSER" ]; then
    CLINTUSER=''
    CLINTGROUP=''
    for VALUE in $CONFUSER
    do
        if [ -z "$CLINTUSER" ]; then CLINTUSER=$VALUE
        else CLINTGROUP=$VALUE ; fi
    done
fi


# Help/usage information.
usage ()
{
    echo "
Clintosaurous Apache 2 environment installation.

This can be reran at any time to validate environment is setup.

sudo `basename $0` [-h | --help] \\
    [ -A | --no-apt-update \\
    [ -S | --server-name \\
    [ -a | --server-admin \\
    [ -k | --ssl-key /key/file/path.key \\
    [ -c | --ssl-cert /cert/file/path.pem \\
    [ -U | --user ] username \\
    [ -G | --group ] group \\
    [ -I | --ignore-os

    -h | --help
        Display this help message.
    -A | --no-apt-update
        Skip updating the aptitude repository and installing system updates.
    -S | --server-name
        FQDN of Apache server.
    -a | --server-admin
        Email address of the server administratory.
    -k | --ssl-key
        Path to HTTPS SSL key file. Default: $KEYFILE
    -c | --ssl-cert
        Path to HTTPS SSL certificate file. Default: $CERTFILE
    -U | --username
        Username to use for the Clintosaurous tools. This must match on all
        servers that run the Clintosaurous environment. It is recommended to
        use the default username. Default: $CLINTUSER
    -G | --group
        User's group name. It is recommended use the default.
        Default: $CLINTGROUP
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
        "-S") shift ; SERVERNAME=$1 ;;
        "--server-name") shift ; SERVERNAME=$1 ;;
        "-a") shift ; SERVERADMIN=$1 ;;
        "--server-admin") shift ; SERVERADMIN=$1 ;;
        "-k") shift; KEYFILE=$1 ;;
        "--ssl-key") shift; KEYFILE=$1 ;;
        "-c") shift; CERTFILE=$1 ;;
        "--ssl-cert") shift; CERTFILE=$1 ;;
        "-U") shift ; CLINTUSER=$1 ;;
        "--user") shift; CLINTUSER=$1 ;;
        "-G") shift ; CLINTGROUP=$1 ;;
        "--group") shift ; CLINTGROUP=$1 ;;
        "-I") IGNOREOS=1 ;;
        "--ignore-os") IGNOREOS=1 ;;
        *) echo "Unknown CLI option $1" ; echo ; usage ;;
    esac
    shift
done


# Verify running on Ubuntu and supporte version.
if [ -z "$IGNOREOS" ] && \
    [ -z "`egrep -E 'Ubuntu\s+2[02].04' /etc/lsb-release 2>/dev/null`" ]
then
    echo "
Clintosaurous tools only support running on Ubuntu systems. Only tested and
supported on Ubuntu 20.04 and 22.04. It may work on older versions, but has
not been tested and is not supported.

Use -I or --ignore-os to override this error.
" >&2
    exit 1
fi


# Ensure we're logged in as root.
if [ `whoami` != 'root' ]; then
    echo "The installation must be ran as root." >&2
    exit 1
fi


# Header.
echo "#### Clintosaurous Apache 2 initial setup starting ####"


# Install required packages.
echo "#### Installing required aptitude packages ####"
if [ $APTUPDATE ]; then
    echo "Updating system"
    apt update && apt upgrade -y
    if [ $? -ne 0 ]; then
        echo "Error updating aptitude packages" >&2
        exit 1
    fi
fi

echo "Installing required packages"
apt install -y apache2 apache2-suexec-pristine
if [ $? -ne 0 ]; then
    echo "Error installing required aptitude packages" >&2
    exit 1
fi

if [ ! -e /lib/systemd/system/httpd.service ]; then
    ln -s /lib/systemd/system/apache2.service \
        /lib/systemd/system/httpd.service
    systemctl daemon-reload
fi

# Enable Apache modules.
echo "Enabling apache2 modules"
a2enmod auth_form cgi request rewrite session session_cookie ssl socache_shmcb
if [ $? -ne 0 ]; then
    echo "Error enabling Apache 2 required modules" >&2
    exit 1
fi

echo "Enabling Apache 2"
systemctl enable apache2
if [ $? -ne 0 ]; then
    echo "Error enabling Apache 2" >&2
    exit 1
fi


# Ensure repository is cloned and up to date.
if [ -e $COREHOME ]; then
    if [ -e $COREHOME/LICENSE ]; then
        echo "Clintosaurous core directory directory exists"
        echo "Ensuring up to date"
        # Must be ran as Clintosaurous user.
        su - -c "cd $COREHOME && git pull" $CLINTUSER
        if [ $? -ne 0 ]; then
            echo "Error updating Clintosaurous core repository" >&2
            exit 1
        fi
    else
        echo "Clintosaurous core directory exists, but is not from the" >&2
        echo "GitHub repository!" >&2
        exit 1
    fi
else
    echo "Clintosaurous core envirnoment must be installed and setup." >&2
    echo "Run the core installation (install.sh) and then retry." >&2
    exit 1
fi

# Ensure configuration file exists. If not, add it and enable it.
if [ ! -e /etc/apache2/sites-available/clintosaurous.conf ]; then
    # Get server name for configuration file.
    if [ -z "$SERVERNAME" ]; then
        echo
        echo -n "Enter server FQDN: " ; read SERVERNAME
    fi
    # Get site admin email for configuration file.
    if [ -z "$SERVERADMIN" ]; then
        echo
        echo -n "Enter server admin email: " ; read SERVERADMIN
    fi

    # Disable the default configuration file.
    if [ -e /etc/apache2/sites-enabled/000-default.conf ]; then
        echo "Disabling Apache 2 default configuration"
        a2dissite 000-default
        if [ $? -ne 0 ]; then
            echo "Error diabling Apache 2 default site" >&2
            exit 1
        fi
    fi

    echo "Adding default configuration file"
    cp $COREHOME/lib/defaults/apache2.conf \
        /etc/apache2/sites-available/clintosaurous.conf

    if [ -e $CERTFILE ]; then
        echo "Certificate exists"
    else
        echo "Adding default web certificate and key"
        cp /opt/clintosaurous/core/lib/defaults/default-www.key $KEYFILE
        cp /opt/clintosaurous/core/lib/defaults/default-www.pem $CERTFILE
        chmod 600 $KEYFILE
        chown $CLINTUSER:$CLINTGROUP $KEYFILE $CERTFILE
    fi

    echo "Setting Apache 2 run time user"
    sed -Ei "s/APACHE_RUN_USER=.+/APACHE_RUN_USER=$CLINTUSER/" \
        /etc/apache2/envvars
    echo "Setting Apache 2 run time group"
    sed -Ei "s/APACHE_RUN_GROUP=.+/APACHE_RUN_GROUP=$CLINTGROUP/" \
        /etc/apache2/envvars
    echo "Setting Apache 2 server name"
    sed -Ei "s/:::server-name:::/$SERVERNAME/" \
        /etc/apache2/sites-available/clintosaurous.conf
    echo "Setting Apache 2 server admin"
    sed -Ei "s/:::server-admin:::/$SERVERADMIN/" \
        /etc/apache2/sites-available/clintosaurous.conf
    echo "Setting Apache 2 SSL key file"
    sed -Ei "s|:::key-file:::|$KEYFILE|" \
        /etc/apache2/sites-available/clintosaurous.conf
    echo "Setting Apache 2 SSL certificate file"
    sed -Ei "s|:::cert-file:::|$CERTFILE|" \
        /etc/apache2/sites-available/clintosaurous.conf

    if [ ! -e /etc/apache2/sites-enabled/clintosaurous.conf ]; then
        echo "Enabling Clintosaurous configuration"
        a2ensite clintosaurous
        if [ $? -ne 0 ]; then
            echo "Error enabling Apache 2 clintosaurous site" >&2
            exit 1
        fi
    fi

    if [ ! -e /etc/apache2/htaccess ]; then
        echo "Setting up Clintosaurous user for web access"
        echo
        htpasswd -c /etc/apache2/htaccess $CLINTUSER
        if [ $? -ne 0 ]; then
            echo "Error creating Apache 2 user $CLINTUSER" >&2
            exit 1
        fi
        chmod 660 /etc/apache2/htaccess
        chown $CLINTUSER:$CLINTGROUP /etc/apache2/htaccess
    fi
fi


# Ensure web index.cgi configuration directory.
if [ -e $ETCDIR/www ]; then
    echo "WWW index page configuration directory exists"
else
    INDEXDIR=/etc/clintosaurous/www
    echo "Creating WWW index configuration directory $INDEXDIR"
    mkdir $INDEXDIR
    if [ $? -ne 0 ]; then
        echo "Error creating WWW index configuration directory" >&2
        exit 1
    fi
    cp $COREDIR/lib/defaults/root-index.conf $ETCDIR/www/
    chown -R $CLINTUSER:$CLINTGROUP $ETCDIR/www
    chmod g+w $ETCDIR/www
fi


ARELOAD=1
if [ ! -e "$KEYFILE" ]; then
    echo "SSL key file $KEYFILE does not exist" >&2
    echo "Update Apache 2 configuration with correct key location, or" >&2
    echo "place key at $KEYFILE" >&2
    ARELOAD=0
fi
if [ ! -e "$CERTFILE" ]; then
    echo "SSL certificate file $CERTFILE does not exist" >&2
    echo "Update Apache 2 configuration with correct certificate" >&2
    echo "location, or place key at $KEYFILE" >&2
    ARELOAD=0
fi

if [ $ARELOAD -ne 0 ]; then
    echo "Restarting Apache 2 service"
    systemctl restart apache2
    if [ $? -ne 0 ]; then
        echo "Error enabling Apache 2 clintosaurous site" >&2
        echo "Check Apache 2 service status or error log for more details" >&2
    fi
fi


echo "#### Clintosaurous Apache 2 setup complete ####"
