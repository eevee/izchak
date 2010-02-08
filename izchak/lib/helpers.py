"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password
from webhelpers.html import escape, literal
from webhelpers.html.tags import *

### Display
def format_float(n):
    """Convenience formatter.  Cuts floats to two places."""
    # Might be getting a literal() object from the template; forcefully
    # try to make it a float first
    return "{0:0.2f}".format(float(n))

def format_commify(n):
    """Sticks commas in a number."""
    s = unicode(n)

    # Take care of decimals
    float_part = '0'
    if '.' in s:
        s, float_part = s.split('.', 1)

    # Break the number into three-digit chunks, then join with a comma
    chunks = []

    while len(s) > 3:
        chunks.insert(0, s[-3:])
        s = s[0:-3]
    chunks.insert(0, s)

    result = ','.join(chunks)

    # Reappend any decimal part
    if float_part and int(float_part) != 0:
        result = '.'.join([result, float_part])

    return result

### TIME STUFF
datetime_format = "%b %e '%y, %H:%M"
time_format = "%H:%M"

def timedelta_to_seconds(td):
    """Returns the numbers of seconds in a timedelta.

    Ignores microseconds."""
    return td.days * 86400 + td.seconds

def divide_timedeltas(td1, td2):
    """Divides two timedelta objects."""
    return 1.0 * timedelta_to_seconds(td1) / timedelta_to_seconds(td2)

### Gameplay-related
def end_type_icon(end_type):
    """Returns an icon appropriate to the given end type."""
    if end_type.identifier == 'ascension':
        icon = u'trophy'
    elif end_type.identifier == 'escape':
        icon = u'door-open-out'
    elif end_type.identifier == 'quit':
        icon = u'cross-small'
    elif end_type.identifier == 'trickery':
        icon = u'wand'
    elif end_type.identifier == 'panic':
        icon = u'bomb'
    else:
        # Regular deaths need no icon
        return u''

    return image("/icons/{0}.png".format(icon),
                 alt=end_type.identifier,
                 title=end_type.identifier)
