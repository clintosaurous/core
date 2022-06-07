#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
pymysql helper module to simplify database connectivity.
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
import clintosaurous.file
import clintosaurous.log as log
import clintosaurous.opts
import pymysql
import yaml


# Predefined variables.
_core_conf = '/etc/clintosaurous/clintosaurous.yaml'


# CLI options.
_parser_db_group = \
    clintosaurous.opts.parser.add_argument_group("database options")
_parser_db_group.description = """
    Data base connectivity options. These are not required on the command
    line and can be supplied during database connection setup.
"""

_parser_db_group.add_argument(
    "--db-host",
    help=f"""
        Database server DNS name or IP address. No default, but a default
        can be supplied in {_core_conf} using the 'db-host' option.
    """,
    type=str
)
_parser_db_group.add_argument(
    "--db-user",
    help=f"""
        Database server name. No default, but a default can be supplied in
        {_core_conf} using the 'db-user' option.
    """,
    type=str
)
_parser_db_group.add_argument(
    "--db-passwd",
    help=f"""
        Database user password. No default, but a default can be supplied in
        {_core_conf} using the 'db-passwd' option.
    """,
    type=str
)
_parser_db_group.add_argument(
    "--db-name",
    help='Database name. Default: None.',
    type=str
)

_parser_db_group.add_argument(
    "--db-ssl",
    help="""
        Enable MySQL SSL connectivity. Default: False, but can be set in
        {_core_conf} using the 'db-ssl' option.
    """,
    action="store_true"
)
_parser_db_group.add_argument(
    "--db-ssl-ca",
    help=f"""
        Path to SSL certificate authority (CA) file for the SSL certificate.
        Default: None, but can be set in {_core_conf} using the 'db-ssl-ca'
        option.
    """,
    type=str
)
_parser_db_group.add_argument(
    "--db-ssl-cert",
    help=f"""
        Path to SSL certificate file for the SSL certificate.
        Default: None, but can also be set in {_core_conf} using the
        'db-ssl-cert' option.
    """,
    type=str
)
_parser_db_group.add_argument(
    "--db-ssl-key",
    help=f"""
        Path to SSL certificate private key file for the SSL certificate.
        Default: None, but can also be set in {_core_conf} using the
        'db-ssl-key' option.
    """,
    type=str
)

# End CLI options


class connect:

    """
    Connects to the a MySQL database using the supplied configuration.

    Almost all options can be set by passing parameters to the function, CLI
    options, and Clintosaurous core configuration file. Values are set
    in the 'database' section of the core configuration file. Remember to
    change from underscores to dashes in configuration file.

    Check order for a value is:
        1.  Function variable.
        2.  CLI option.
        3.  Clintosaurous core configuration file.

    host: Database server DNS name or IP.

    user
        Username for connecting to the database. See --db-user CLI
        option help. Default: None

    passwd
        Password for above username. Default: None

    database
        Name of the database to use. See --db-name CLI option help.

    ssl
        Enable/disable MySQL connection encryption. See --db-ssl CLI
        option help. Default: None

    ssl_ca
        See --db_ssl_ca CLI option help.

    ssl_cert
        See --db_ssl_cert CLI option help.

    ssl_key
        See --db_ssl_key CLI option help.

    autocommit
        Boolean to enable or disable autocommit. Autocommit is disabled by
        default.

    connect_timeout
        Connection timeout in seconds. Default is 10.

    logging
        Boolean to enable/disable operation logging. Helpful in scripts
        that are not using logging or a web application.
    """

    def __init__(
        self,
        host=None,
        user=None,
        passwd=None,
        database=None,
        ssl=None,
        ssl_ca=None,
        ssl_cert=None,
        ssl_key=None,
        autocommit=False,
        connect_timeout=10,
        logging=True
    ):

        opts = clintosaurous.opts.cli()

        with open(_core_conf, newline='') as c:
            conf = yaml.safe_load(c)

        options = [
            ["host", host, opts.db_host, True, None],
            ["database", database, opts.db_name, True, None],
            ["user", user, opts.db_user, True, None],
            ["passwd", passwd, opts.db_passwd, True, None],
            ["ssl", ssl, opts.db_ssl, False, False],
            ["ssl-ca", ssl_ca, opts.db_ssl_ca, False, None],
            ["ssl-cert", ssl_cert, opts.db_ssl_cert, False, None],
            ["ssl-key", ssl_key, opts.db_ssl_key, False, None],
            ["autocommit", autocommit, None, False, False],
            ["connect-timeout", connect_timeout, None, True, None]
     ]
        try:
            db_conf = conf["database"]
        except KeyError:
            db_conf = {}
        self._check_opts(options, db_conf)
        self.options["autocommit"] = autocommit
        self.options["connection-timeout"] = connect_timeout

        self.connect_opts = {
            "host": self.options["host"],
            "user": self.options["user"],
            "password": self.options["passwd"],
            "database": self.options["database"],
            "autocommit": self.options["autocommit"],
            "connect_timeout": self.options["connect-timeout"]
        }
        if self.options["ssl"]:
            self.connect_opts["ssl"] = {"ssl": {
                "ca": self.options["ssl-ca"],
                "cert": self.options["ssl-cert"],
                "key": self.options["ssl-key"]
            }}

        if logging:
            log.log(
                'Connecting to database ' +
                f'{self.options["user"]}@{self.options["host"]}/' +
                self.options["database"]
            )

        self.connection = pymysql.connect(**self.connect_opts)

    # End __int__()

    def _check_opts(self, options, conf):

        # Set connection option values for connecting to database.
        self.options = {}
        for name, passed, cli, required, default in options:
            if passed is not None:
                self.options[name] = passed
            elif cli is not None:
                    self.options[name] = cli
            else:
                try:
                    self.options[name] = conf[name]
                except KeyError:
                    if default is not None:
                        self.options[name] = default
                    elif required:
                        raise ValueError(f'{name} not supplied')

    # End: _check_opts()

# End class connect
