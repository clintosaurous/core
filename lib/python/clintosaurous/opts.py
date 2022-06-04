#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
This module provides CLI argument parsing functionality for Clintosaurous
tools scripts.

See argparse documention for details on parser syntax and usage.

    clintosaurous.opts.parser

    argparse_parser = opts.parser

    argparse parser object for adding script specific options.
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
import argparse


# Predefined variables.
parser = argparse.ArgumentParser()
cli_opts = None


def cli():

    """
    Parse the CLI options from the arguments passed on the CLI.
    """

    global cli_opts
    global parser

    if cli_opts:
        return cli_opts

    cli_opts = parser.parse_args()

    return cli_opts

# End cli()
