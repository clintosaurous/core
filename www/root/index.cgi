#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
This module facilitates creating web pages in the Clintosaurous tools
enviroment.

    import clintosaurous.cgi
    cgi = clintosaurous.cgi.cgi(opt, ...)
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
import clintosaurous.cgi
import yaml


if __name__ == "__main__":
    cgi = clintosaurous.cgi.cgi({
        "title": "Clint's Home Network Login",
        "version": VERSION,
        "last_update": LAST_UPDATE,
        "copyright": 2022
    })

    print(cgi.start_page())

    conf_file = cgi.form_values.getvalue("conf")
    if conf_file is None:
        conf_file = '/etc/clintosaurous/www/www-root-index.yaml'
    with open(conf_file, newline='') as c:
        conf = yaml.safe_load(c)
    print(cgi.index_list(conf))

    print(cgi.end_page())
