import os
import re
import sys
from unidecode import unidecode

def clean_tweet(
    text,
    replace_by_space=['/','(',')',',','#',"'"],
):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    q = " ".join(new_text)
    replace_by_space=['/','(',')',',',"'",'#']
    for c in replace_by_space:
        q = q.replace(c, ' ')
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
