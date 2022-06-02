#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
Web login page for home network Apache servers.
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


def form_options():

    return {
        "method": 'post',
        "action": '/dologin.html',
        "fields": [
            {
                "type": 'text',
                "name": 'httpd_username',
                "title": 'Username'
            },
            {
                "type": 'password',
                "name": 'httpd_password',
                "title": 'Password'
            }
        ],
        "hidden": [{"name": 'login', "value": 'Login', "override": True}],
        "buttons": [{"name": 'login_button', "value": 'Login'}]
    }

# End: form_options()


if __name__ == "__main__":
    cgi = clintosaurous.cgi.cgi(
        title="Clintosaurous Tools Login",
        version=VERSION,
        last_update=LAST_UPDATE,
        copyright=2022
    )

    print(cgi.start_page())
    print(cgi.form(**form_options()))
    print(cgi.end_page())
