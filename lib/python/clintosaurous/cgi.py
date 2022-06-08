#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
This module facilitates creating web pages in the Clintosaurous tools
enviroment.

    import clintosaurous.cgi
    cgi = clintosaurous.cgi.cgi(opt, ...)
    print(cgi.start_page())
    print('<p>Hello World!</p>')
    print(cgi.end_page())

It support starting and ending a page, forms, and text tables.

See /opt/clintosaurous/www/styles/standard.css for available classes.
"""

# Version: 1.0.0
# Last Updated: 2022-06-07
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-06-07)
#
# Note: See repository commit logs for change details.


# Required modules.
import cgi as cgi_mod
import cgitb
import clintosaurous.datetime as datetime
import html
import os
import re
import random


# Base class for the module.
class cgi:

    """
    Base class for CGI operations.

    Initialize clintosaurous.cgi object.

        import clintosaurous.cgi
        cgi = clintosaurous.cgi.cgi(opts, ...)

    contact
        Contact for web page in the HTML header.

    title
        Title for the header of the web page.

    header
        Boolean of whether to gernate a header for the page.

    home_url
        The URL to use for when someone clicks on the logo.

    icon
        Tab icon to display.

    css
        Relative path to the style sheet to use for page.

    css_android
        Relative path to the style sheet to use for page on Android devices.

    version
        Calling script version.

    last_update
        Calling script last updated date.

    copywrite
        Copyright year of the calling script.
    """

    def __init__(
        self, title, contact=None, header=True, home_url=None,
        icon='/images/logo.ico',
        logo='/images/logo.ico', css='/styles/standard.css',
        css_android='/styles/standard-android.css', version=None,
        last_update=None, copyright=None
    ):

        # Save init call arguments.
        self.title = title
        self.contact = contact
        self.header = header
        self.home_url = home_url
        self.icon = icon
        self.logo = logo
        self.css = css
        self.version = version
        self.last_update = last_update
        self.copyright = copyright

        # Build full URL. Used for forms.
        http_script_name = os.environ.get("SCRIPT_NAME")
        if http_script_name is None:
            http_script_name = '/'
        self.url = "{}://{}{}".format(
            os.environ.get("REQUEST_SCHEME"),
            os.environ.get("HTTP_HOST"),
            http_script_name
        )

        # Parse the CGI environment.
        self.env = cgi_mod.parse()
        # Parse URL parameters.
        self.form_values = cgi_mod.FieldStorage()

        # Check if requesting device is an Android device, and update the CSS
        # file to Android specific file.
        usr = os.getenv("HTTP_USER_AGENT")
        if usr is not None and re.search(r'Android', usr):
            self.css = css_android

    # End __init__()


    def end_page(self):

        """
        End an HTML page. Version, last updated, etc. uses the values supplied
        in clintosaurous.cgi.cgi(opts).

            print(cgi.end_page())
        """

        # Build page end summary.
        return_txt = f"""
</div>

<div class="footer">
{self.hr()}
<p class="footer">
"""

        # Add version and last updated information to output if supplied. Last
        # updated is only output if a version is supplied.
        if self.version is not None:
            return_txt += f'Version {self.version}'

            # Add last updated to output if supplied. 
            if self.last_update:
                return_txt += f', Updated {self.last_update}<br>\n'
            else:
                return_txt += '<br>\n'

        # Add the script start time and run time to output.
        return_txt += '{}, {}'.format(
            datetime.timestamp(datetime.start_time),
            datetime.run_time()
        )

        # Add username to output.
        if os.getenv("REMOTE_USER"):
            user = os.getenv("REMOTE_USER").split("@", 1)[0]
            return_txt += f', Logged in as: {user}'

        # Add copyright notice to output if copyright year supplied.
        if self.copyright:
            return_txt += (
                '<br>\n' +
                f'Copyright {self.copyright} by Clinton R McGraw. ' +
                ' All Rights Reserved.'
            )

        # Close the HTML.
        return_txt += """
</p>
</div>

</body>
</html>
"""

        return return_txt

    # End: end_page()


    def error_msg(self, msg):

        """
        Ouput a formatted error message.

            print(cgi.error_msg(string))
        """

        return f'<p class="error_message\">{msg}</p>\n'

    # End: error_msg()


    def escape(self, decoded):

        """
        Escapes HTML string special characters.
        """

        return html.escape(decoded)

    # End: escape_html()


    def form(
        self, title=None, comment=None, name=None, hidden=None, fields=None,
        buttons=None, action=None, method='put'
    ):

        """
        Builds a web form using the parameters supplied.

            print(cgi.form(opt, ...))

        Either buttons or fields is required.

            title
                Form title to display above the form.

            comment
                Comment to add under the title and before the actual form.

            name
                Name of the form. If omitted, a random name will be assigned.

            hidden
                List of hidden fields to add to the form. See below for more
                information on the options.

            fields
                List of fields to add to the form. See below for more
                information on the options.

            buttons
                List of buttons to add to the form. See below for more
                information on the options.

            action
                URL to send a form submit to. Default: Same URL as the form.

            method
                Submit method, put/post. Default: 'put'

        buttons:

            List of dictionaries with button data. They will be displayed in
            the order of the list.

            name and value are required.

                buttons = [
                    {
                        "button_type": "submit"
                        "name": None,
                        "value": None
                    }
                ]


                button_type
                    HTML type of form button.

                name
                    HTML value name.

                value
                    Value of the button that is displayed.

        fields:

            List of dictionaries with form field data. They will be displayed
            in the order of the list.

            Form field types:
                -   checkbox
                -   dropdown
                -   list
                -   radio
                -   text|password
                -   textarea

            title, type, and name are required values.

            The fields have an "override" option to override the received
            value. By default, if the form has already been submitted, the
            value from that submittion is used as the default value. This can
            overriden with the "override" option. The functions will use the
            value defined in the "value" option, not the "default".

            fields = [

                {
                    "type": "checkbox",
                    "title": None,      # Display text next to the checkbox.
                    "checked": False,   # Default to box unchecked.
                    "name": None,       # HTML tag name.
                    "value": None,      # Value of a checked box.
                    "override": False   # Override previous submit value.
                },

                {
                    "type": "dropdown|list",    # Difference is in the CSS
                                                # class the list is assigned.
                    "title": None,      # Display text next to the dropdown.
                    "name":             # HTML tag name.
                    "values": None,     # Required list of dropdown values.
                    "labels": None,     # Optional dictionary relating the
                                        # value in "values" to their display
                                        # name. If omitted, "values" will be
                                        # the value and the display name.
                    "default": None,    # Default value selected.
                    "override": False   # Override previous submit default
                                        # value.
                },

                {
                    "type": "text|password",    # password ignores previous
                                                # submit value.
                    "title": None,      # Display text next to the text field.
                    "name": None,       # HTML tag name.
                    "value": None,      # Default value for text box.
                    "maxlength": None,  # Maximum string length in text field.
                    "override": False   # Override previous submit value.
                },

                {
                    "type": "textarea",
                    "title": None,      # Display text next to the textarea.
                    "name": None,       # HTML tag name.
                    "value": None,      # Default value for text box.
                    "cols": 40,         # Number of text columns in area.
                    "rows": 5,          # Number text rows in area.
                    "override": False   # Override previous submit value.
                },

                {
                    "type": "radio",
                    "title": None,      # Display text next to the dropdown.
                    "name":             # HTML tag name.
                    "values": None,     # Required list of dropdown values.
                    "labels": None,     # Optional dictionary relating the
                                        # value in "values" to their display
                                        # name. If omitted, "values" will be
                                        # the value and the display name.
                    "default": None,    # Default value selected.
                    "override": False   # Override previous submit default
                                        # value.
                }

            ]

        hidden:

            List of dictionaries with form hidden field data.

                hidden = [
                    {
                        "name":         # HTML tag name.
                        "value": None   # Default value for hidden field.
                    }
                ]
        """

        # Verify we were provided basic form data. Either fields or buttons
        # are required.
        if fields is None and buttons is None:
            raise ValueError('fields or buttons values are required')

        # If no action supplied, default to self.
        if action is None:
            action = self.url

        # Generate random form name if no form name is supplied.
        if name is None:
            name = f'form_{random.randrange(0, 100000)}'

        method = method.lower()
        return_txt = '<div class="input_form">'

        # If fields were supplied, they will go in a table. Start the table.
        # If only buttons are supplied, we do not need a table.
        if fields is not None:
            return_txt += '<table class="input_form">\n'

        # Start the web form.
        return_txt += \
            f'<form action="{action}" name="{name}" method="{method}">\n'

        # Process fields.
        return_txt += self._form_hidden(hidden) + '\n'
        return_txt += self._form_fields(fields) + '\n'

        # Process form buttons.
        if buttons is not None:
            # If there are form fields, start table row.
            if fields is not None:
                return_txt += (
                    '<tr class="form_button">' +
                    '<td class="form_buttons" colspan="2">\n'
                )

            return_txt += self._form_buttons(buttons) + '\n'

            # If fields exist, close the HTML table row.
            if fields is not None:
                return_txt += "</td></tr>\n"

        return_txt += '</form>'

        # If fields, close out the table.
        if fields is not None:
            return_txt += '</table>\n'

        return_txt += '</div>'

        # Generate a text box with the form information.
        return self.text_box(return_txt, title=title, comment=comment)

    # End: form()


    def _form_buttons(self, buttons):

        # Internal function for building form button fields.

        return_txt = ''

        # Build HTML for the form buttons.
        for button in buttons:
            try:
                button_type = button["button_type"]
            except KeyError:
                button_type = "submit"
            return_txt += (
                f'<input type="{button_type}" name="{button["name"]}" ' +
                f'value="{button["value"]}" />\n'
            )

        return return_txt

    # End: _form_buttons()


    def _form_check_override(self, field):

        # Check if "override" was specified, or default to False.
        try:
            override = field["override"]
        except KeyError:
            override = False

        # If overriding form value, set to supplied "value", or default to ''.
        if override:
            try:
                return field["value"], True
            except KeyError:
                return '', True

        # If not overriding, check if a form submition value exists. If so,
        # default to that, or default to ''. 
        else:
            value = self.form_values.getvalue(field["name"])
            if value is None:
                try:
                    return field["default"], False
                except KeyError:
                    return '', False
            return value, False

    # End: _form_check_override()


    def _form_fields(self, fields):

        # Internal function for building out form fields.

        if fields is None:
            return ''

        return_txt = ''

        # Loop through fields supplied.
        for field in fields:
            # Start new HTML table row for each field.
            return_txt += f"""
                <tr class="field_row">
                <td class="form_field_title">{field["title"]}:</td>
                <td class="field_input">
            """

            # Check for value override.
            value, override = self._form_check_override(field)

            # HTML text or password field.
            if field["type"] == 'text' or field["type"] == 'password':
                return_txt += (
                    f'<input type="{field["type"]}" ' +
                    f'name="{field["name"]}" value="{value}"'
                )

                # Add field max length if supplied.
                try:
                    return_txt += f' maxlength="{field["maxlength"]}"'
                except KeyError:
                    True

                return_txt += ' />\n'

            # HTML text area field.
            elif field["type"] == 'textarea':
                # Set default columns and rows for the text area.
                try:
                    field["cols"]
                except KeyError:
                    field["cols"] = 40
                try:
                    field["rows"]
                except KeyError:
                    field["rows"] = 5

                return_txt += (
                    f'<textarea name="{field["name"]}" ' +
                    f'cols="{field["cols"]}" rows="{field["rows"]}" ' +
                    f'class="field_input">{value}</textarea>\n'
                )

            # HTML dropdown or list field.
            elif field["type"] == 'dropdown' or field["type"] == 'list':
                values = field["values"]
                try:
                    labels = field["labels"]
                except KeyError:
                    labels = {}
                    for l_value in values:
                        labels[l_value] = l_value

                if field["type"] == 'dropdown':
                    field_class = "field_input"
                else:
                    field_class = "field_list"

                return_txt += \
                    f'<select name="{field["name"]}" class="{field_class}">'

                for f_value in values:
                    if not isinstance(value, str):
                        value = str(value)

                    return_txt += f'<option value="{value}"'
                    if f_value == value:
                        return_txt += ' selected="selected"'
                    return_txt += f'>{labels[value]}</option>\n'

                return_txt += '</select>\n'

            # HTML checkbox.
            elif field["type"] == 'checkbox':
                # Check for value override.
                if override:
                    try:
                        form_checked = field["checked"]
                    except KeyError:
                        checked = ''
                    else:
                        if form_checked:
                            checked = " checked"
                        else:
                            checked = ''
                else:
                    if value != '':
                        try:
                            form_checked = field["checked"]
                        except KeyError:
                            checked = ''
                        else:
                            if form_checked:
                                checked = " checked"
                            else:
                                checked = ''
                    else:
                        checked = " checked"

                return_txt += (
                    f'<label><input type="checkbox" name="{field["name"]}" ' +
                    f'value="{value}" ' +
                    f'class="field_input"{checked} /></label>\n'
                )

            # HTML radio button.
            elif field["type"] == 'radio':
                buttons = []
                try:
                    labels = field["labels"]
                except KeyError:
                    labels = {}
                    for l_value in field["values"]:
                        labels[l_value] = l_value

                for f_value in field["values"]:
                    if f_value == value:
                        checked = ' checked'
                    else:
                        checked = ''

                    buttons.append(
                        f'<input type="radio"{checked} ' +
                        f'name="{field["name"]}" value="{f_value}">' +
                        f'{labels[f_value]}</input>\n'
                    )

                return_txt += '<div>\n' + '<br>\n'.join(buttons) + '</div>\n'

            return_txt += "</td>\n</tr>\n"

        return return_txt

    # End: _form_fields()


    def _form_hidden(self, fields):

        # Internal function for outputting form hidden fields.

        if fields is None:
            return ''

        return_txt = ''

        for field in fields:
            # Check for value override.
            value, override = self._form_check_override(field)
            return_txt += (
                f'<input type="hidden" name="{field["name"]}" ' +
                f'value="{value}" />\n'
            )

        return return_txt

    # End: _form_hidden()


    def hr(self, class_name="divider"):

        """
        Returns a horizontal (<hr>) bar string.

            print(cgi.hr())
        """

        return f'<hr class="{class_name}" />\n'

    # End: hr()


    def _index_list(self, list_data, new_level=True):

        """
        Internal function to build an index list for index.cgi.
        """

        return_txt = ''

        return_txt += '<ul class="index_list">\n'

        for entry in list_data:

            return_txt += '<li class="list_index">'

            if new_level:
                return_txt += '<p class="list_index">\n'

            try:
                return_txt += f'<a href="{entry["link"]}">'
                return_txt += f'{entry["title"]}</a></li>\n'

            except KeyError:
                return_txt += entry["title"]

            try:
                return_txt += self._index_list(entry["links"], False)
            except KeyError:
                True

            if new_level:
                return_txt += '</p>\n'

        return_txt += '</ul>\n'

        return return_txt

    # End: _index_list()


    def index_list(self, list_data):

        """
        Build an index page.

            print(cgi.index_list(list_data))

        list_data is a list of dictionaries with list data. This support
        multilevels of menus.

            list_data = [
                {
                    "title": None,
                    "link": None,
                    "links": [
                        {
                            "title": None,
                            "link": None,
                            "links": None
                        }
                    ]
                }
            ]

            title
                Required title to be displayed for the menu item.

            link
                Optional link for the entry.

            links
                Array for nested menu items. It has the same format as
                list_data. There is no preset limit on nested entries.
        """

        return_txt = (
            '<div class="index_list"><p class="index_list">\n' +
            self._index_list(list_data) +
            '</p></div>\n'
        )

        return return_txt

    # End: index_list()


    def start_page(self):

        """
        Start an HTML page.

            print(cgi.start_page())

        Values from cgi.cgi().
        """

        cgitb.enable()

        # Start HTML text page and open <head>.
        return_txt = f"""Content-Type: text/html

<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head>
    <title>{self.title}</title>
"""

        # Add page contact if supplied.
        if self.contact is not None:
            return_text += \
                f'    <link rev="made" href="mailto:{self.contact}" />'

        # Finish <head> and open <body>
        return_txt += f"""
    <link href="{self.icon}" rel="icon" />
    <link rel="stylesheet" type="text/css" href="{self.css}" />
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
</head>

<body>

"""

        # Check if the page header should be displayed. Add page header.
        header = self.form_values.getvalue("header")
        if header is None or (header != "0" and header.upper() != "FALSE"):
            return_txt += f"""
<div class="header">
<table class="header"><tr class="header">
    <td class="logo"><a href="{self.home_url}">
        <img src="{self.logo}" alt="Logo" class="logo" height="100">
    </a></td>
    <td class="title"><h1 class="title">{self.title}</h1></td>
</tr></table>
</div>

"""

        return_txt += "<div class=\"page_content\">\n"

        return return_txt

    # End: start_page()


    def table(self, rows, headings=True):

        """
        Build an HTML table.

            print(cgi.table())

        Arguments:

            -   rows
                    List of lists with possible headings and row values.

            -   headings
                    Boolean if the first row in rows is a headings row.
        """

        return_txt = """
            <div class="data_table">
            <table class="data_table">
        """

        cur_row = 0

        if headings:
            cur_row += 1
            return_txt += '<tr class="data_table_heading">\n'
            for value in rows[0]:
                return_txt += f'<td class="data_table_heading">{value}</td>\n'
            return_txt += "</tr>\n"

        for row_num in range(cur_row, len(rows)):
            return_txt += '<tr class="data_table_data">\n'
            for value in rows[row_num]:
                return_txt += f'<td class="data_table_data">{value}</td>\n'
            return_txt += "</tr>\n"

        return_txt += """
            </table>
            </div>
        """

        return return_txt

    # End: table()


    def table_split(self, rows, headings=True, sections=3):

        """
        Splits a table into multiple tables. Like cgi.table(), this will split
        the data into X number of columns instead of all one column. It will
        replicate the headings to each split block if headings are supplied.

            print(table_split(rows))

        Arguments:

            -   rows
                    List of lists with possible headings and row values.

            -   headings
                    Boolean if the first row in rows is a headings row.
                    Default: True

            -   sections
                    How many sectiosn to split the data in to.
                    Default: 3
        """

        total_rows = int(len(rows))
        rows_per_column = int(total_rows / sections)
        if total_rows % sections != 0:
            rows_per_column += 1

        if headings:
            headings = row[0]
            del row[0]

        table = []
        table_rows = [[] for i in range(sections)]
        out_tables = []
        cur_table = 0
        for row in rows:
            table = table_rows[cur_table]
            table.append(row)
            if len(table) >= rows_per_column:
                table.insert(0, headings)
                out_tables.append(self.table(table))
                cur_table += 1

        if len(table) < rows_per_column:
            if headings:
                table.insert(0, headings)
            out_tables.append(self.table(table))

        return self.table([out_tables], headings=False)

    # End: table_split()


    def text_box(self, html, title=None, comment=None):

        """
        Build a text box.

            print(cgi.textbox("HTML', 'Title'))

            title
                Optional title to display in the text box.

            html
                HTML to be put in the box contents.

            comment
                HTML formated string to be added between the title and the
                text box.
        """

        return_txt = '<div class="text_box">\n'

        if title is not None:
            return_txt += f'<p class="text_box_title">{title}</p>\n'

        if comment is not None:
            return_txt += f'<p class="comment">{comment}</p>\n'

        return_txt += f'<p class="text_box_txt">{html}</p>\n</dev>\n'

        return return_txt

    # End: text_box()


    def unescape(self, encoded):

        """
        Unescapes and HTML string special characters.
        """

        return html.unescape(encoded)

    # End: encode_html()


# End class cgi
