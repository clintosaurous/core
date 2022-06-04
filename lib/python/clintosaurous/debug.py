#!/opt/clintosaurous/venv/bin/python3 -Bu

"""
Contains functions helpful for debugging.
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
import clintosaurous.text


# Predefined variables.
ascii_table = {
    0:      'NUL',  1:      'SOH',  2:      'STX',  3:      'ETX',
    4:      'EOT',  5:      'ENQ',  6:      'ACK',  7:      'BEL',
    8:      'BS',   9:      'HT',   10:     'LF',   11:     'VT',
    12:     'FF',   13:     'CR',   14:     'SO',   15:     'SI',
    16:     'DLE',  17:     'DC1',  18:     'DC2',  19:     'DC3',
    20:     'DC4',  21:     'NAK',  22:     'SYN',  23:     'ETB',
    24:     'CAN',  25:     'EM',   26:     'SUB',  27:     'ESC',
    28:     'FS',   29:     'GS',   30:     'RS',   31:     'US',
    32: 'Space',    33:     '!',    34:     '"',    35:     '#',
    36:     '$',    37:     '%',    38:     '&',    39:     '\'',
    40:     '(',    41:     ')',    42:     '*',    43:     '+',
    44:     ',',    45:     '-',    46:     '.',    47:     '/',
    48:     '0',    49:     '1',    50:     '2',    51:     '3',
    52:     '4',    53:     '5',    54:     '6',    55:     '7',
    56:     '8',    57:     '9',    58:     ':',    59:     ';',
    60:     '<',    61:     '=',    62:     '>',    63:     '?',
    64:     '@',    65:     'A',    66:     'B',    67:     'C',
    68:     'D',    69:     'E',    70:     'F',    71:     'G',
    72:     'H',    73:     'I',    74:     'J',    75:     'K',
    76:     'L',    77:     'M',    78:     'N',    79:     'O',
    80:     'P',    81:     'Q',    82:     'R',    83:     'S',
    84:     'T',    85:     'U',    86:     'V',    87:     'W',
    88:     'X',    89:     'Y',    90:     'Z',    91:     '[',
    92:     '\\',   93:     ']',    94:     '^',    95:     '_',
    96:     '`',    97:     'a',    98:     'b',    99:     'c',
    100:    'd',    101:    'e',    102:    'f',    103:    'g',
    104:    'h',    105:    'i',    106:    'j',    107:    'k',
    108:    'l',    109:    'm',    110:    'n',    111:    'o',
    112:    'p',    113:    'q',    114:    'r',    115:    's',
    116:    't',    117:    'u',    118:    'v',    119:    'w',
    120:    'x',    121:    'y',    122:    'z',    123:    '{',
    124:    '|',    125:    '}',    126:    '~',    127:    'DEL;',
    128:    '€',    # Euro sign
    129:    'N/A',  # (Not in use)
    130:    '‚',    # Single low-9 quotation mark
    131:    'ƒ',    # Latin small letter f with hook
    132:    '„',    # Double low-9 quotation mark
    133:    '…',    # Horizontal ellipsis
    134:    '†',    # Dagger
    135:    '‡',    # Double dagger
    136:    'ˆ',    # Modifier letter circumflex accent
    137:    '‰',    # Per mille sign
    138:    'Š',    # Latin capital letter S with caron
    139:    '‹',    # Single left-pointing angle quotation
    140:    'Œ',    # Latin capital ligature OE
    141:    'N/A',  # (Not in use)
    142:    'Ž',    # captial letter Z with caron
    143:    'N/A',  # (Not in use)
    144:    'N/A',  # (Not in use)
    145:    '‘',    # Left single quotation mark
    146:    '’',    # Right single quotation mark
    147:    '“',    # Left double quotation mark
    148:    '”',    # Right double quotation mark
    149:    '•',    # Bullet
    150:    '–',    # En dash
    151:    '—',    # Em dash
    152:    '˜',    # Small tilde
    153:    '™',    # Trade mark sign
    154:    'š',    # Latin small letter S with caron
    155:    '›',    # Single right-pointing angle quotation mark
    156:    'œ',    # Latin small ligature oe
    157:    'N/A',  # (Not in use)
    158:    'ž',    # small letter z with caron
    159:    'Ÿ',    # Latin capital letter Y with diaeresis
    160:    'NBS',  # Non-breaking space
    161:    '¡',    # Inverted exclamation mark
    162:    '¢',    # Cent sign
    163:    '£',    # Pound sign
    164:    '¤',    # Currency sign
    165:    '¥',    # Yen sign
    166:    '¦',    # Pipe, Broken vertical bar
    167:    '§',    # Section sign
    168:    '¨',    # Spacing diaeresis - umlaut
    169:    '©',    # Copyright sign
    170:    'ª',    # Feminine ordinal indicator
    171:    '«',    # Left double angle quotes
    172:    '¬',    # Not sign
    173:    '­',     # Soft hyphen
    174:    '®',    # Registered trade mark sign
    175:    '¯',    # Spacing macron - overline
    176:    '°',    # Degree sign
    177:    '±',    # Plus-or-minus sign
    178:    '²',    # Superscript two - squared
    179:    '³',    # Superscript three - cubed
    180:    '´',    # Acute accent - spacing acute
    181:    'µ',    # Micro sign
    182:    '¶',    # Pilcrow sign - paragraph sign
    183:    '·',    # Middle dot - Georgian comma
    184:    '¸',    # Spacing cedilla
    185:    '¹',    # Superscript one
    186:    'º',    # Masculine ordinal indicator
    187:    '»',    # Right double angle quotes
    188:    '¼',    # Fraction one quarter
    189:    '½',    # Fraction one half
    190:    '¾',    # Fraction three quarters
    191:    '¿',    # Inverted question mark
    192:    'À',    # Latin capital letter A with grave
    193:    'Á',    # Latin capital letter A with acute
    194:    'Â',    # Latin capital letter A with circumflex
    195:    'Ã',    # Latin capital letter A with tilde
    196:    'Ä',    # Latin capital letter A with diaeresis
    197:    'Å',    # Latin capital letter A with ring above
    198:    'Æ',    # Latin capital letter AE
    199:    'Ç',    # Latin capital letter C with cedilla
    200:    'È',    # Latin capital letter E with grave
    201:    'É',    # Latin capital letter E with acute
    202:    'Ê',    # Latin capital letter E with circumflex
    203:    'Ë',    # Latin capital letter E with diaeresis
    204:    'Ì',    # Latin capital letter I with grave
    205:    'Í',    # Latin capital letter I with acute
    206:    'Î',    # Latin capital letter I with circumflex
    207:    'Ï',    # Latin capital letter I with diaeresis
    208:    'Ð',    # Latin capital letter ETH
    209:    'Ñ',    # Latin capital letter N with tilde
    210:    'Ò',    # Latin capital letter O with grave
    211:    'Ó',    # Latin capital letter O with acute
    212:    'Ô',    # Latin capital letter O with circumflex
    213:    'Õ',    # Latin capital letter O with tilde
    214:    'Ö',    # Latin capital letter O with diaeresis
    215:    '×',    # Multiplication sign
    216:    'Ø',    # Latin capital letter O with slash
    217:    'Ù',    # Latin capital letter U with grave
    218:    'Ú',    # Latin capital letter U with acute
    219:    'Û',    # Latin capital letter U with circumflex
    220:    'Ü',    # Latin capital letter U with diaeresis
    221:    'Ý',    # Latin capital letter Y with acute
    222:    'Þ',    # Latin capital letter THORN
    223:    'ß',    # Latin small letter sharp s - ess-zed
    224:    'à',    # Latin small letter a with grave
    225:    'á',    # Latin small letter a with acute
    226:    'â',    # Latin small letter a with circumflex
    227:    'ã',    # Latin small letter a with tilde
    228:    'ä',    # Latin small letter a with diaeresis
    229:    'å',    # Latin small letter a with ring above
    230:    'æ',    # Latin small letter ae
    231:    'ç',    # Latin small letter c with cedilla
    232:    'è',    # Latin small letter e with grave
    233:    'é',    # Latin small letter e with acute
    234:    'ê',    # Latin small letter e with circumflex
    235:    'ë',    # Latin small letter e with diaeresis
    236:    'ì',    # Latin small letter i with grave
    237:    'í',    # Latin small letter i with acute
    238:    'î',    # Latin small letter i with circumflex
    239:    'ï',    # Latin small letter i with diaeresis
    240:    'ð',    # Latin small letter eth
    241:    'ñ',    # Latin small letter n with tilde
    242:    'ò',    # Latin small letter o with grave
    243:    'ó',    # Latin small letter o with acute
    244:    'ô',    # Latin small letter o with circumflex
    245:    'õ',    # Latin small letter o with tilde
    246:    'ö',    # Latin small letter o with diaeresis
    247:    '÷',    # Division sign
    248:    'ø',    # Latin small letter o with slash
    249:    'ù',    # Latin small letter u with grave
    250:    'ú',    # Latin small letter u with acute
    251:    'û',    # Latin small letter u with circumflex
    252:    'ü',    # Latin small letter u with diaeresis
    253:    'ý',    # Latin small letter y with acute
    254:    'þ',    # Latin small letter thorn
    255:    'ÿ'     # Latin small letter y with diaeresis
}
# End ascii_table


def ascii_str_table(usr_text):

    """
    Takes the string supplied and converts it to table of the ASCII values
    of each character.

        >>> import clint.base
        >>> debug = clint.debug
        >>>
        >>> print(debug.ascii_str_table("Test string.\\n"))
        +---------------+
        |  String ASCII |
        |    Values     |
        +-------+-------+
        | Index | Char  |
        +-------+-------+
        | 0     | T     |
        | 1     | e     |
        | 2     | s     |
        | 3     | t     |
        | 4     | Space |
        | 5     | s     |
        | 6     | t     |
        | 7     | r     |
        | 8     | i     |
        | 9     | n     |
        | 10    | g     |
        | 11    | .     |
        | 12    | LF    |
        +-------+-------+
    """

    split_text = [char for char in usr_text]
    rows = []

    for i in range(len(split_text)):
        rows.append([i, ascii_table[ord(split_text[i])]])

    headings = ['Index', 'Char']

    return clintosaurous.text.table('String ASCII Values', headings, rows)

# End ascii_str_table()
