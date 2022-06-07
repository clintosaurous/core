#!/opt/clintosaurous/venv/bin/python3 -Bu

""" Functions for e-mail services. """

# Version: 1.0.0
# Last Updated: 2022-05-30
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-30)
#
# Note: See repository commit logs for change details.


# Required modules.
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from os.path import basename
import smtplib
import yaml


# Predefined variables.
_core_conf = '/etc/clintosaurous/clintosaurous.yaml'


def send(
    to_addr=None,
    subject=None,
    text=None,
    attachments=[],
    server=None,
    from_addr=None,
    html=True
):

    """
    Send an e-mail using the supplied options. Currently does not support
    SMTP server login.

    to_addr
        E-Mail address(es) to send to. Comma separated. Default: None

    subject
        E-Mail subject. Default: None

    text
        E-Mail body text. Default: None

    attachments
        List of files to attach to the e-mail. Defaut: None

    server
        FQDN or IP of the SMTP server to connect to. Default: localhost,
        , but can be set in /etc/clintosaurous/clintosaurous.yaml with 'server' under
        the 'email' section.

    from_addr
        E-Mail address to send e-mail from. Default: None, but can be set
        in /etc/clintosaurous/clintosaurous.yaml with 'from' under the 'email'
        section.

    html
        Boolean of if email text is HTML. Default: True
    """

    with open(_core_conf, newline='') as y:
        conf = yaml.safe_load(y)

    if to_addr is None:
        raise ValueError('Missing to email address') 

    if from_addr is None:
        try:
            from_addr = conf["email"]["from"]
        except KeyError:
            raise ValueError('Missing from email address') 

    if server is None:
        try:
            server = conf["email"]["server"]
        except KeyError:
            raise ValueError('Missing SMTP server name') 

    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject

    if html:
        msg.attach(MIMEText(text, "html"))
    else:
        msg.attach(MIMEText(text))

    for file_name in attachments:
        with open(file_name, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(file_name)
            )
        # After the file is closed
        part['Content-Disposition'] = \
            'attachment; filename="%s"' % basename(file_name)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(from_addr, to_addr, msg.as_string())
    smtp.close()

# End send()
