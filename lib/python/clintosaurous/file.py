#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
Common Clintosaurous tools file functions.
"""

# Version: 1.0.0
# Last Updated: 2022-06-04
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-06-04)
#
# Note: See repository commit logs for change details.


# Required modules.
import atexit
import clintosaurous.datetime
import clintosaurous.log as log
import os
import re
import sys


# Predefined variables.
lock_file = "/run/lock/{0}.pid".format(os.path.basename(sys.argv[0]))


def datestamp(usr_time=None):

    """
    Returns a datestamp to be used for a file name. A Unix style timestamp
    can be supplied, otherwise current time is used.

        >>> import clint.base
        >>> file = clint.file()
        >>>
        >>> file.datestamp()
        '2020-08-27'
    """

    return clintosaurous.datetime.datestamp(usr_time)

# End: datestamp()


def lock():

    """
    Checks if a current lock file exists. If the lock file exists, it checks
    if the PID in the lock file is still running. If it is not a warning is
    thrown and a new lock file is created. If it is still running, the script
    will throw an error and die.

    Lock file path will be placed at /run/lock/<script_name>.pid.

    Lock file will be removed on clean exit, or can be removed manually using
    clint.file.unlock().

    Lock file path can be found at clint.file.lock_file.
    """

    global lock_file

    pid = os.getpid()

    if os.path.exists(lock_file):
        file_obj = open(lock_file)
        file_pid = file_obj.read()
        file_obj.close()
        file_pid = int(file_pid.strip())
        if file_pid == pid:
            return

        try:
            os.kill(file_pid, 0)

        except OSError:
            log.warn("Lock file exists, but process dead. Overriding lock.")
            os.remove(lock_file)

        else:
            log.error("Existing process {0} running!".format(file_pid))
            quit(1)

    with open(lock_file, "w") as file_obj:
        file_obj.write(str(pid))

    atexit.register(unlock)

# End: lock()


def timestamp(usr_time=None, tz=True):

    """
    Returns a timestamp to be used for a file name. A Unix style timestamp
    can be supplied, otherwise current time is used.

    user_time
        User specified Unix formatted timestamp.
    tz
        Boolean of whether to add timezone to end of timestamp. Default: True

        >>> import clint.base
        >>> file = clint.file()
        >>>
        >>> file.timestamp()
        '2020-08-27-15-52-52-edt'
    """

    return re.sub(
        r'\W+', '-',
        clintosaurous.datetime.timestamp(usr_time, tz=tz).lower()
    )

# End: timestamp()


def unlock():

    """
    Removes the script lock file.
    """

    global lock_file

    if os.path.exists(lock_file):
        os.remove(lock_file)

# End: unlock()
