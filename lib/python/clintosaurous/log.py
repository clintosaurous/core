#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
This module provides logging functionality for Clintosaurous tools.

Facilitates logging functions.

    +-------------------+
    |     Log Levels    |
    +---------+---------+
    | 0 = EMR | 4 = WRN |
    | 1 = ALR | 5 = LOG |
    | 2 = CRI | 6 = INF |
    | 3 = ERR | 7 = DBG |
    +---------+---------+

Log level (5) is the default log level.
"""

# Version: 1.0.0
# Last Updated: 2022-05-30
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-30)
#
# Note: See repository commit logs for change details.


# Required modules.
import clintosaurous.opts
import clintosaurous.datetime
import os
import sys
import syslog as slog


# CLI options.
_parser_log_group = clintosaurous.opts.parser.add_argument_group("logging")

_parser_log_group.add_argument(
    "-d", "--debug",
    action="store_true",
    help="Set logging level to debug."
)
_parser_log_group.add_argument(
    "--log-append",
    action="store_true",
    help="""
        Append existing log file if it exists. Default is to create a new
        file.
    """
)
_parser_log_group.add_argument(
    "--log-file",
    type=str,
    help="Output log file name. If omitted, STDOUT and STDERR used."
)
_parser_log_group.add_argument(
    "-i", "--log-info",
    action="store_true",
    help="Set logging level to info. Is overwridden by --debug."
)
_parser_log_group.add_argument(
    "--log-level",
    default=5,
    type=int,
    help="""
        Set the default logging level using the logging level integer value.
        Is overwridden by --debug. Default is 5 (LOG).
    """
)
_parser_log_group.add_argument(
    "--no-log-stderr",
    action="store_true",
    help="Disables sending error messages to STDERR. Output to STDOUT only."
)
_parser_log_group.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="""
        Set logging to quiet. Only output error messages or more severe
        (level 4 or lower). Overrides --log_level, --log_info, and --debug.
    """
)
_parser_log_group.add_argument(
    "-S", "--silent",
    action="store_true",
    help="Suppresses all logging output."
)
_parser_log_group.add_argument(
    "-s", "--syslog",
    action="store_true",
    help="Output log messages to syslog, not STDOUT/STDERR."
)


# Predefined variables.
log_levels = ["EMR", "ALR", "CRI", "ERR", "WRN", "LOG", "INF", "DBG"]
_out_level = False
_syslog_proc = os.path.basename(sys.argv[0])
_syslog_levels = [
    slog.LOG_EMERG, slog.LOG_ALERT, slog.LOG_CRIT, slog.LOG_ERR,
    slog.LOG_WARNING, slog.LOG_NOTICE, slog.LOG_INFO, slog.LOG_DEBUG
]


def emr(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied to STDERR. This is an
    emergency level (level 0) entry. Multiline strings will have an entry for
    each line in the string. Multiple messages can be given.

    It will still be output with the --quiet CLI option is supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(0, msgs, syslog=syslog)

# End log.emr()


def alr(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied to STDERR. This is an
    alarm level (level 1) entry. Multiline strings will have an entry for each
    line in the string. Multiple messages can be given.

    This will not be output unless --log_level is 1 or higher, --log_info, or
    the --debug CLI option is supplied. It will still be output with the
    --quiet CLI option is supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(1, msgs, syslog=syslog)

# End log.alr()


def cri(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied to STDERR. This is a
    critical level (level 2) entry. Multiline strings will have an entry for
    each line in the string. Multiple messages can be given.

    This will not be output unless --log_level is 2 or higher, --log_info, or
    the --debug CLI option is supplied. It will still be output with the
    --quiet CLI option is supplied.

    Unless 'exit' is set to False or --no_log_die is provided at the CLI, the
    script will exit with an exit code of 1.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(2, msgs, syslog=syslog)

# End log.cri()


def err(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied to STDERR. This is an
    error level (level 3) entry. Multiline strings will have an entry for each
    line in the string. Multiple messages can be given.

    Unless 'exit' is set to False or --no_log_die is provided at the CLI, the
    script will exit with an exit code of 1.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(3, msgs, syslog=syslog)

# End log.err()


def wrn(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied to STDERR. This is a
    warning level (level 4) entry. Multiline strings will have an entry for
    each line in the string. Multiple messages can be given.

    This will not be output unless --log_level is 3 or higher, --log_info, or
    the --debug CLI option is supplied. It will still be output with the
    --quiet CLI option is supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(4, msgs, syslog=syslog)

# End log.wrn()


def log(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied. This is a log level
    (level 5) entry. Multiline strings will have an entry for each line in
    the string. Multiple messages can be given.

    This will not be output unless --log_level is 5 or higher, --log_info, or
    the --debug CLI option is supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(5, msgs, syslog=syslog)

# End log.log()


def inf(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied. This is an
    informational level (level 6) entry. Multiline strings will have an entry
    for each line in the string. Multiple messages can be given.

    This will not be output unless --log_level is 6 or higher, --log_info, or
    the --debug CLI option is supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(6, msgs, syslog=syslog)

# End log.inf()


def dbg(msgs, syslog=False):

    """
    Outputs a log message with the log message supplied. This is a debug
    level (level 7) entry. Multiline strings will have an entry for each line
    in the string. Multiple messages can be given.

    This will not be output unless --log_level is 7 or the --debug CLI options
    are supplied.

    if syslog is set to True, messages are output to syslog, not
    STDOUT/STDERR.
    """

    if msgs:
        _msg_out(7, msgs, syslog=syslog)

# End log.debug()


def log_level():

    """
    Get the configured log level based on CLI options.
    """

    global _out_level

    if _out_level:
        return _out_level

    opts = clintosaurous.opts.cli()

    if (
        opts.log_file
        and os.path.exists(opts.log_file)
        and not opts.log_append
    ):
        os.remove(opts.log_file)

    _out_level = opts.log_level
    if opts.silent:
        _out_level = -1
    elif opts.quiet:
        _out_level = 4
    elif opts.log_info:
        _out_level = 6
    elif opts.debug:
        _out_level = 7

    return _out_level

# End log_level


def _msg_out(level, msgs, syslog=False, exit=False):

    global log_levels, _syslog_levels, _syslog_proc

    if not isinstance(msgs, list):
        msgs=[msgs]

    _out_level = log_level()
    if level > _out_level:
        return

    opts = clintosaurous.opts.cli()

    timestamp = clintosaurous.datetime.timestamp()

    display_level = log_levels[level]
    if opts.log_file:
        out = open(opts.log_file, "a")
    elif opts.no_log_stderr or level >= 5:
        out = sys.stdout
    else:
        out = sys.stderr

    for msg in msgs:
        for line in msg.split("\n"):
            if syslog or opts.syslog:
                slog.openlog(_syslog_proc, facility=slog.LOG_LOCAL2)
                slog.syslog(_syslog_levels[level], line.strip())
                slog.closelog()
            else:
                out.write(f'{timestamp}: {display_level}: {line.rstrip()}\n')

    if opts.log_file:
        out.close()

# End _msg_out()
