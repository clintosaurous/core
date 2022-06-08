#!/bin/sh

# Commonly used functions and variables in Clintosaurous shell scripts.
#
# Version: 1.0.0
# Last Updated: 2022-05-30
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-30)
#
# Note: See repository commit logs for change details.


# Global variables.
export CLINTHOME=/opt/clintosaurous
export CLINTCORE=$CLINTHOME/core
export CLINTETC=/etc/clintosaurous
export CLINTLOG=/var/log/clintosaurous
export _STARTDATETIME=`date +%s`


check_login_user () {
    if [ -z "$1" ]; then
        echo "You must supply a username to check_login_user()" >&2
        exit 1
    elif [ "`whoami`" != "$1" ]; then
        echo "You must be $1 to run this!" >&2
        exit 1
    fi
}   # End function check_root


check_valid_os () {
    ERRMSG="Running unsupported OS or OS version. Only Ubuntu 20.04 or 22.04"
    ERRMSG="$ERRMSG are supported. The tools may run on other OSes, but they"
    ERRMSG="$ERRMSG have not been tested and are not currently supported."
    if [ ! -e /etc/os-release ]; then
        echo $ERRMSG >&2
        exit 1
    fi
    . /etc/os-release
    if [ ! "`echo "$PRETTY_NAME" | egrep 'Ubuntu 2[02].04'`" ]; then
        echo $ERRMSG >&2
        exit 1
    fi
}


# Outputs a date stamp in YYYY-MM-DD format.
datestamp ()
{
    echo `date +%F`
    return
}


# Output supplied error message(s) and exit with exit code 1.
error_out ()
{

    for ARG ; do
        echo $ARG >&2
    done

    exit 1

}   # End function error_out


# Output supplied log message(s) with prepended timestamps.
log_msg ()
{

    DATETIME=`timestamp`

    for ARG
    do
        echo "${DATETIME}: ${ARG}"
    done

}   # End function log_msg


# Output log message(s) supplied via STDIN with prepended timestamps.
log_stdin ()
{

    DATETIME=`timestamp`

    while read LINE
    do
        if [ -n "$LINE" ]; then
            echo "${DATETIME}: ${LINE}"
        fi
    done

}   # End function log_msg


# Output the current run time of the script.
run_time ()
{

    _CURRENTDATETIME=`date +%s`
    echo `expr \( $_CURRENTDATETIME - $_STARTDATETIME \) | seconds_breakdown`

}


# Output a breakdown of seconds into minutes, hours, and days.
seconds_breakdown ()
{

    SECS=$1
    MINS=0
    HRS=0
    DAYS=0

    MIN=60
    HR=3600
    DAY=86400

    if [ -z $SECS ] ; then
        read -p "Enter number of seconds: " SECS
        if [ -z $SECS ] ; then
            echo "You must enter or supply the number of seconds to " \
                "breakdown!"
            return
        fi
    fi

    if [ $SECS -ge $DAY ] ; then
        DAYS=`expr \( \( $SECS - $SECS % $DAY \) / $DAY \)`
        SECS=`expr \( $SECS % $DAY \)`
    fi

    if [ $SECS -ge $HR ] ; then
        HRS=`expr \( \( $SECS - $SECS % $HR \) / $HR \)`
        SECS=`expr \( $SECS % $HR \)`
    fi

    if [ $SECS -ge $MIN ] ; then
        MINS=`expr \( \( $SECS - $SECS % $MIN \) / $MIN \)`
        SECS=`expr \( $SECS % $MIN \)`
    fi

    if [ $DAYS -gt 0 ] ; then
        DATA="$DAYS day"
        if [ $DAYS -ne 1 ] ; then DATA="${DATA}s" ; fi
        if [ $SECS -gt 0 ] ; then
            DATA="${DATA}, ${HRS} hour"
            if [ $HRS -ne 1 ] ; then DATA="${DATA}s" ; fi
            DATA="${DATA}, ${MINS} minute"
            if [ $MINS -ne 1 ] ; then DATA="${DATA}s" ; fi
            DATA="${DATA}, ${SECS} second"
            if [ $SECS -ne 1 ] ; then DATA="${DATA}s" ; fi
        elif [ $MINS -gt 0 ] ; then
            DATA="${DATA}, ${HRS} hour"
            if [ $HRS -ne 1 ] ; then DATA="${DATA}s" ; fi
            DATA="${DATA}, ${MINS} minute"
            if [ $MINS -ne 1 ] ; then DATA="${DATA}s" ; fi
        elif [ $HRS -gt 0 ] ; then
            DATA="${DATA}, ${HRS} hour"
            if [ $HRS -ne 1 ] ; then DATA="${DATA}s" ; fi
        fi

    elif [ $HRS -gt 0 ] ; then
        DATA="$HRS hour"
        if [ $HRS -ne 1 ] ; then DATA="${DATA}s" ; fi
        if [ $SECS -gt 0 ] ; then
            DATA="${DATA}, ${MINS} minute"
            if [ $MINS -ne 1 ] ; then DATA="${DATA}s" ; fi
            DATA="${DATA}, ${SECS} second"
            if [ $SECS -ne 1 ] ; then DATA="${DATA}s" ; fi
        elif [ $MINS -gt 0 ] ; then
            DATA="${DATA}, ${MINS} minute"
            if [ $MINS -ne 1 ] ; then DATA="${DATA}s" ; fi
        fi

    elif [ $MINS -gt 0 ] ; then
        DATA="$MINS minute"
        if [ $MINS -ne 1 ] ; then DATA="${DATA}s" ; fi
        if [ $SECS -gt 0 ] ; then
            DATA="${DATA}, ${SECS} second"
            if [ $SECS -ne 1 ] ; then DATA="${DATA}s" ; fi
        fi

    else
        DATA="$SECS second"
        if [ $SECS -ne 1 ] ; then DATA="${DATA}s" ; fi
    fi

    echo $DATA

}   # End function seconds_breakdown


# Output a timestamp in logging format.
timestamp ()
{

    date +"%F %T %Z"

}   # End function timestamp


# Help.
_usage ()
{
    SCRIPTNAME=`basename $0`
    echo "
Shell script include library of commonly used functions and variables by
Clintosaurous IPAM scripts.

$SCRIPTNAME [-h | --help]
. $SCRIPTNAME

Variabls:
    LOG_DIR
        Logging directory location.
    PATH
        Updated as needed.
    PYTHONPATH
        Updated as needed.

Functions:
    datestamp
        Outputs a date stamp in YYYY-MM-DD format.
    error_out
        Echoes the error message to STDERR prepending a timestamp of the
        current time and exits with code 1. If multiple messages supplied,
        all will be echoed on seperate lines each prepended with a timestamp.
    timestamp
        Echoes the current local time in Perl localtime format.
    log_msg
        Echoes the message supplied to STDOUT prepending a timestamp. If
        multiple messages supplied, all will be echoed on seperate lines each
        prepended with a timestamp.
    seconds_breakdown
        Takes the number of seconds supplies and breaks it down into days,
        hours, minutes, and seconds and echoes the breakout in the below
        format.
            $ seconds_breakdown 108556
            1 day, 6 hours, 9 minutes, 16 seconds
        Different scenarios will not display full breakout. Examples:
            $ seconds_breakdown 86400
            1 day
            $ seconds_breakdown 568
            9 minutes, 28 seconds
            $ seconds_breakdown 7200
            2 hours
"
    exit

}


# Process CLI options.
if [ "$1" = "--help" ] || [ "$1" = "-h" ] ; then _usage ; fi


# Environment variables.
if [ -z `echo "$PATH" | grep '/opt/clintosaurous/venv/bin'` ]; then
    export PATH="/opt/clintosaurous/venv:$PATH"
fi

if [ -z `echo "$PYTHONPATH" | grep '/opt/clintosaurous/core/lib/python'` ]; then
    export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}/opt/clintosaurous/core/lib/python"
fi
