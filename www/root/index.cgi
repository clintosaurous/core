#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
This module facilitates creating web pages in the Clintosaurous tools
enviroment.

    import clintosaurous.cgi
    cgi = clintosaurous.cgi.cgi(opt, ...)
"""

VERSION = '1.0.0'
LAST_UPDATE = '2022-06-02'
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-06-02)
#
# Note: See repository commit logs for change details.


# Required modules.
import clintosaurous.cgi
import yaml


if __name__ == "__main__":
    cgi = clintosaurous.cgi.cgi(
        title='Clintosaurous Tools',
        version=VERSION,
        last_update=LAST_UPDATE,
        copyright=2022
    )

    print(cgi.start_page())
    print(cgi.hr())

    with open('/etc/clintosaurous/www-index.yaml', newline='') as c:
        conf = yaml.safe_load(c)
    print(cgi.index_list(conf))

    print(cgi.end_page())
