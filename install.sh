#!/bin/sh

# Performs the initial installation and setup of the Clintosaurous core
# environment.
#
# Version: 1.0.0
# Last Updated: 2022-05-30
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-30)
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
#   5.  Create directory structure as needed.
#   6.  Create Clintosaurous group and user. This can be suppressed with CLI
#       options. Skipped if already exists via an `id` command.
#   7.  Clone or Clintosaurous core environment repository.
#   8.  Setup Clintosaurous user's default environment.
#   9.  Create default core configuration file if needed.
#   10. Create `logrotate` configuration file if needed.
#   11. Update ownership and privileges for Clintosaurous directories.
#   12. Create Clintosaurous SSH keys if needed.
#   13. Create Clintosaurous Python VENV if needed.
#   14. Install required PIP modules.
#   15. Add Clintosaurous include to /etc/bash.bashrc, if needed.
#   16. Validate root and clintosaurous user crontab.


# Environment setup.
APTUPDATE=1
CREATEUSER=1
IGNOREOS=0
REPOUPDATE=1
CLINTUSER=clintosaurous
CLINTGROUP=clintosaurous
USERHOME=/opt/clintosaurous
COREHOME=$USERHOME/core
BASHINC=$COREHOME/lib/bash/bashrc
PYLIB=$COREHOME/lib/python
ETCDIR=/etc/clintosaurous
LOGDIR=/var/log/clintosaurous


# Help/usage information.
usage ()
{
    echo "
Clintosaurous core environment installation.

This can be reran at any time to validate environment is setup.

sudo `basename $0` [-h | --help] \\
    [ -A | --no-apt-update \\
    [ -N | --no-create-user ] \\
    [ -R | --no-repo-update \\
    [ -U | --user ] username \\
    [ -u | --uid ] UID \\
    [ -p | --group ] group \\
    [ -g | --gid ] GID \\
    [ -I | --ignore-os \\
    [ -b | --branch ] branch-name

    -h | --help
        Display this help message.
    -A | --no-apt-update
        Skip updating the aptitude repository and installing system updates.
    -N | --no-create-user
        Skip checking for and creating user and user group.
    -R | --no-repo-update
        Skip performing a git pull to update the existing repository.
    -U | --username
        Username to use for the Clintosaurous tools. This must match on all
        servers that run the Clintosaurous environment. It is recommended to
        use the default username. Default: $CLINTUSER
    -u | --uid
        Set the user ID (UID) for user Clintosaurous for if user needs to be
        created. Default: Set by adduser command.
    -p | --group
        User's group name. It is recommended use the default.
        Default: $CLINTGROUP
    -g | --gid
        Set the user group ID (GID) for user Clintosaurous for if user needs
        to be created. Default: Set by addgroup command.
    -I | --ignore-os
        Suppress checking OS and OS version. Although checks are suppressed,
        the command set only supports Debian based hosts.
    -b | --branch
        Set the GitHub repository branch to use. Default: main

Paths are statically set. Below are the base directories created:
    $USERHOME: $CLINTUSER's home directory.
    $ETCDIR: Configuration file storage.
    $LOGDIR: Logs directory.
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
        "-N") CREATEUSER=0 ;;
        "--no-create-user") CREATEUSER=0 ;;
        "-R") REPOUPDATE=0 ;;
        "--no-repo-update") REPOUPDATE=0 ;;
        "-U") shift ; CLINTUSER=$1 ;;
        "--user") shift; CLINTUSER=$1 ;;
        "-u") shift ; USERUID=$1 ; CLIUID="--uid $1";;
        "--uid") shift ; USERUID=$1 ; CLIUID="--uid $1" ;;
        "-p") shift ; CLINTGROUP=$1 ;;
        "--group") shift ; CLINTGROUP=$1 ;;
        "-g") shift ; USERGID=$1 ; CLIGID="--gid $1" ;;
        "--gid") shift ; USERGID=$1 ; CLIGID="--gid $1" ;;
        "-I") IGNOREOS=1 ;;
        "--ignore-os") IGNOREOS=1 ;;
        "-b") shift ; BRANCH=$1 ;;
        "--branch") shift ; BRANCH=$1 ;;
        *) echo "Unknown CLI option $1" ; echo ; usage ;;
    esac
    shift
done


# Verify running on Ubuntu and supporte version.
if [ $IGNOREOS -eq 0 ]; then
    if [ ! -e /etc/lsb-release ]; then
        echo "
    lsb-release missing!

    Install and retry.

    apt install -y lsb-release
    " >&2
        exit 1
    elif [ -z "`egrep -E 'Ubuntu\s+2[02].04' /etc/lsb-release 2>/dev/null`" ]
    then
        echo "
    Clintosaurous tools only support running on Ubuntu systems. Only tested and
    supported on Ubuntu 20.04 and 22.04. It may work on older versions, but has
    not been tested and is not supported.

    Use -I or --ignore-os to override this error.
    " >&2
        exit 1
    fi
fi


# Ensure we're logged in as root.
if [ `whoami` != 'root' ]; then
    echo "The installation must be ran as root." >&2
    exit 1
fi


# Header.
echo "#### Clintosaurous core initial setup starting ####"
echo "Clintosaurous home directory: $USERHOME"
echo "Clintosaurous core directory: $COREHOME"


# Install required packages.
if [ $APTUPDATE -ne 0 ]; then
    echo "#### Installing required aptitude packages ####"
    echo "Updating system"
    apt update && apt upgrade -y
    if [ $? -ne 0 ]; then
        echo "Error updating aptitude packages" >&2
        exit 1
    fi

    echo "Installing required packages"
    apt install -y \
        curl \
        dkms \
        git \
        g++ \
        gawk gawk-doc \
        gcc \
        make \
        mysql-client \
        net-tools \
        python3 \
            python3-doc python3-pip python3-venv python3-magic python3-pymysql \
        traceroute \
        unzip \
        wget
    if [ $? -ne 0 ]; then
        echo "Error installing required aptitude packages" >&2
        exit 1
    fi
fi


# Validate directories exist.
echo "#### Validating directories exist ####"
for DIR in $USERHOME $ETCDIR $LOGDIR
do
    if [ -e $DIR ]; then
        echo "Directory $DIR exists"
    else
        echo "Creating $DIR directory"
        mkdir $DIR
        if [ $? -ne 0 ]; then
            echo "Error creating directory $DIR" >&2
            exit 1
        fi
    fi
done


# Setup user and group.
if [ $CREATEUSER -ne 0 ]; then
    echo "#### Setting up $CLINTUSER user and group ####"
    if [ -n "`id $CLINTUSER 2>/dev/null | grep 'uid='`" ]; then
        echo "User $CLINTUSER already exits"
    else
        echo "Creating group $CLINTGROUP"
        addgroup $CLIGID $CLINTGROUP
        if [ $? -ne 0 ]; then
            echo "Error adding group $CLINTGROUP" >&2
            exit 1
        fi

        echo "Creating $CLINTUSER user"
        USERGID=`grep "$CLINTUSER:" /etc/group | sed -re 's/^.+:([0-9]+):$/\1/'`
        CLIGID="--gid $USERGID"
        adduser --shell /bin/bash --home $USERHOME --no-create-home \
            $CLIGID $CLIUID $CLINTUSER
        if [ $? -ne 0 ]; then
            echo "Error adding user $CLINTUSER" >&2
            exit 1
        fi
    fi
else
    echo "#### Skipping user creation from CLI option ####"
fi


echo "#### Setting up core environment ####"

# Reset directory ownership to be able to clone repository.
echo "Setting directory ownership to $CLINTUSER:$CLINTGROUP"
chown -R $CLINTUSER:$CLINTGROUP $USERHOME $ETCDIR $LOGDIR
chmod -R g+w,o= $ETCDIR


# Ensure repository is cloned.
if [ $REPOUPDATE -ne 0 ]; then
    if [ -e $COREHOME ]; then
        if [ -e $COREHOME/LICENSE ]; then
            echo "Clintosaurous core directory directory exists"
            echo "Ensuring up to date"
            cd $COREHOME
            if [ -n "$BRANCH" ]; then
                su - -c "cd $COREHOME && git checkout $BRANCH" $CLINTUSER
                if [ $? -ne 0 ]; then
                    echo "Error changing Clintosaurous core repository branch" >&2
                    exit 1
                fi
            fi
            su - -c "cd $COREHOME && git pull" $CLINTUSER
            if [ $? -ne 0 ]; then
                echo "Error updating Clintosaurous core repository" >&2
                exit 1
            fi
        else
            echo "
    Clintosaurous core directory exists, but is not from from the GitHub
    repository!" >&2
            exit 1
        fi
    else
        echo "Cloning Clintosaurous core repository"
        # Must be ran as Clintosaurous user.
        su - -c "git clone https://github.com/clintosaurous/core.git $COREHOME" \
            $CLINTUSER
        if [ $? -ne 0 ]; then
            echo "Error cloning Clintosaurous core repository" >&2
            exit 1
        fi
        if [ -n "$BRANCH" ]; then
            su - -c "cd $COREHOME && git checkout $BRANCH" $CLINTUSER
            if [ $? -ne 0 ]; then
                echo "Error changing Clintosaurous core repository branch" >&2
                exit 1
            fi
        fi
    fi
fi

echo "Validating core configuration files exist"
CORECONF=$ETCDIR/clintosaurous.yaml
if [ -e $CORECONF ]; then
    echo "$CORECONF exists"
else
    echo "Creating default configuraiton file at $CORECONF"
    cp /opt/clintosaurous/core/lib/defaults/clintosaurous.yaml $CORECONF
    if [ $? -ne 0 ]; then
        echo "Error creating core configuration file $CORECONF" >&2
        exit 1
    fi
    sed -Ei "s|<<<CLINTUSER>>>|$CLINTUSER|" $CORECONF
    sed -Ei "s|<<<CLINTGROUP>>>|$CLINTGROUP|" $CORECONF
fi

echo "Checking default user environment environment files"
for FILE in bashrc my.cnf profile
do
    DEFFILE=$COREHOME/lib/defaults/$FILE
    UFILE=$USERHOME/.$FILE
    if [ !-e $UFILE ]; then
        echo "Copying $DEFFILE to $UFILE"
        cp $DEFFILE $UFILE
        if [ $? -ne 0 ]; then
            echo "Error copying $DEFFILE" >&2
            exit 1
        fi
    fi
done

echo "Validating core configuration file exists"
LOGROTATE=/etc/logrotate.d/clintosaurous-core
if [ -e $LOGROTATE ]; then
    echo "$LOGROTATE exists"
else
    echo "Copying logrotate file to $LOGROTATE"
    cp $COREHOME/lib/defaults/logrotate $LOGROTATE
    chmod 644 $LOGROTATE
fi

# Reset directory ownership.
echo "Setting directory ownership to $CLINTUSER:$CLINTGROUP"
chown -R $CLINTUSER:$CLINTGROUP $USERHOME $ETCDIR $LOGDIR
if [ $? -ne 0 ]; then
    echo "Error setting owner to $CLINTUSER:$CLINTGROUP" >&2
    exit 1
fi
echo "Updating directory and file permissions"
chmod -R g+w,o-w $USERHOME $ETCDIR $LOGDIR
chmod g+s $ETCDIR $LOGDIR

# Setting up SSH keys is done after ownership/permissions are set.
echo "#### Setting up SSH keys ####"
if [ -e "$USERHOME/.ssh/id_rsa" ]; then
    echo "SSH keys already exist"
else
    echo "Generating SSH keys"
    # Must be ran as Clintosaurous user.
    su - -c "ssh-keygen -b 2024 -N '' -f $USERHOME/.ssh/id_rsa" clintosaurous
    if [ $? -ne 0 ]; then
        echo "Error generating clintosaurous SSH keys" >&2
        exit 1
    fi
fi


echo "#### Setting Python virtual environment ####"
VENVDIR=$USERHOME/venv
if [ -e "$VENVDIR" ]; then
    echo "Python virtual environment exists"
else
    echo "Creating Python virtual environment to $VENVDIR"
    # Must be created as Clintosaurous user.
    su - -c "python3 -m venv $VENVDIR" clintosaurous
    if [ $? -ne 0 ]; then
        echo "Error creating Python VENV" >&2
        exit 1
    fi
fi

echo "Installing required modules"
# Must be ran as Clintosaurous user.
su - -c ". $VENVDIR/bin/activate && python3 -m pip install cryptography pymysql pyyaml" \
    clintosaurous
if [ $? -ne 0 ]; then
    echo "Error installing Python modules" >&2
    exit 1
fi


echo "#### Validate /etc/bash.bashrc include ####"
if [ -n "`grep $BASHINC /etc/bash.bashrc`" ]; then
    echo "$BASHINC in /etc/bash.bashrc"
else
    echo "Adding $BASHINC to /etc/bash.bashrc"
    echo "
# Clintosaurous environment include script.
. $BASHINC" >> /etc/bash.bashrc
fi


echo "#### Validating crontabs ####"
for U in root $CLINTUSER
do
    echo "Processing crontab for $U"
    CRONTAB="`crontab -u $U -l 2>&1`"
    if [ "$CRONTAB" = "no crontab for $U" ]; then
        echo "Installing default crontab for $U"
        crontab -u $U $COREHOME/lib/defaults/crontab
        if [ $? -ne 0 ]; then
            echo "Error installing $U crontab" >&2
            exit 1
        fi
    else
        PYPATH="`echo \"$CRONTAB\" | egrep 'PYTHONPATH='`"
        if [ -n "$PYPATH" ]; then
            if [ -z "`echo $PYPATH | grep $PYLIB`" ]; then
                echo "PYTHONPATH missing Clintosaurous core in $U's crontab"\
                    >&2
                echo "   Append '$PYLIB' to PYTHONPATH in $U's crontab" >&2
            fi
        else
            echo "PYTHONPATH missing in $U crontab" >&2
            echo "   Add 'PYTHONPATH=$PYLIB' at the top of $U's crontab" >&2
        fi

        if [ -n "`echo \"$CRONTAB\" | grep CLINTCORE`" ]; then
            echo "CLINTCORE set in $U's crontab"
        else
            echo "$U crontab exists but missing CLINTCORE." >&2
            echo "Add 'CLINTCORE=$CLINTCORE'" >&2
            echo "to the beginning of $U's crontab." >&2
        fi

        if [ -n "`echo \"$CRONTAB\" | grep LOGDIR`" ]; then
            echo "LOGDIR set in $U's crontab"
        else
            echo "$U crontab exists but missing LOGDIR." >&2
            echo "Add 'LOGDIR=$LOGDIR'" >&2
            echo "to the beginning of $U's crontab." >&2
        fi
    fi
done

echo "#### Core setup complete ####"
