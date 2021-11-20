import os
import re
import sys
from unidecode import unidecode

def clean_tweet(
    q,
    replace_by_space=['/','(',')',',','#',"'"],
    remove = [],
    extra_w = ['+','-'],
    keep = ["+",'-','.','"']
):
    q = unidecode(q)
    q = q.lower()
    for c in replace_by_space:
        q = q.replace(c, ' ')
    for c in remove:
        q = q.replace(c, '')
    q = re.sub('[^\w{}]+'.format(''.join([re.escape(c) for c in keep])),' ',q)
    q = re.sub('\.\.+','. ',q)
    q = re.sub('\.(?:\s|$)',' ',q)
    q = re.sub('\s+',' ',q)
    q = q.strip()
    return q

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(sys.executable)
    return os.path.dirname(__file__)
