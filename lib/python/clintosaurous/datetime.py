#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
Provides date and time operations for Clintosaurous scripts.
"""

# Version: 1.0.0
# Last Updated: 2022-06-02
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-06-02)
#
# Note: See repository commit logs for change details.


# Required modules.
import time
import clintosaurous.text


# Predefined variables.
#   Script start time for use with run_time()
start_time = time.time()


def datestamp(usr_time=None):

    """
    Generates a datestamp string for the Unix time supplied, or for the
    current date if omitted. Format is "YYYY-MM-DD".

        >>> import datetime as datetime
        >>> datetime.datestamp()
        '2020-08-17'
    """

    if usr_time:
        usr_time = time.localtime(usr_time)
    else:
        usr_time = time.localtime()

    return time.strftime("%Y-%m-%d", usr_time)

# End datestamp()


def run_time(delta_time=None, short=False):

    """
    Returns a string with the run time of the number of seconds provided,
    or since script execution if seconds is omitted. There are two formats
    that can be returned. A long time description or a short one which can be
    specifed with the "short" option.

    Long format: 2 days, 2 hours, 2 minutes, 2 seconds
    Short format: DD:HH:MM:SS

    If there is not a value for one of the timeframes, they will not be returned.
    Exception is seconds is always returned, even if zero.

        >>> import datetime as datetime
        >>> datetime.run_time(86400 * 2 + 3661)
        '2 days, 1 hour, 1 minute, 1 second'
        >>> datetime.run_time(86400 * 2 + 3661, short=True)
        '02:01:01:01'
    """

    if not delta_time:
        global start_time
        delta_time = time.time() - start_time

    days, hours, minutes, seconds = time_breakdown(delta_time)

    return_lables = []
    return_values = []

    if days:
        return_lables.append("day")
        return_values.append(days)

    if hours:
        return_lables.append("hour")
        return_values.append(hours)
    elif short and len(return_values):
        return_values.append(0)

    if minutes:
        return_lables.append("minute")
        return_values.append(minutes)
    elif short:
        return_values.append(0)

    if return_values and not short:
        seconds = int(seconds)

    return_lables.append("second")
    return_values.append(seconds)

    if short:
        for i in range(len(return_values)):
            return_values[i] = str(return_values[i]).rjust(2, '0')
        return ":".join(return_values)

    return_data = []
    for i in range(len(return_lables)):
        return_data.append("{} {}".format(
            return_values[i],
            clintosaurous.text.pluralize(return_lables[i], return_values[i])
        ))

    return ", ".join(return_data)

# End run_time()


def time_breakdown(seconds):

    """
    Breaks down the number of seconds into days, hours, minutes, and
    seconds. All are returned as integer objects.

        >>> import datetime as datetime
        >>> datetime.datetime.time_breakdown(86400 * 2 + 3661)
        (2, 1, 1, 1)
    """

    values = []
    units = [86400, 3600, 60]
    for unit_seconds in units:
        if seconds > unit_seconds:
            values.append(int(seconds / unit_seconds))
            seconds = int(seconds % unit_seconds)
        else:
            values.append(0)

    values.append(seconds)

    return values

# End time_breakdown()


def timestamp(usr_time=None, tz=True):

    """
    Generates a timestamp string for the Unix time supplied or for the
    current date and time if omitted. Format is "YYYY-MM-DD HH:MM:SS TZ".
    TZ is the local system's timezone.

        >>> import datetime as datetime
        >>> datetime = datetime
        >>>
        >>> datetime.timestamp()
        '2020-08-17 15:58:24 EDT'
    """

    if usr_time:
        usr_time = time.localtime(usr_time)
    else:
        usr_time = time.localtime()

    if tz:
        return time.strftime("%Y-%m-%d %H:%M:%S %Z", usr_time)
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S", usr_time)

# End timestamp()
