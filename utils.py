#Utility functions

from markdown import Markdown
from io import StringIO

import string

#non-alphanumeric characters
badchars = ''.join(c for c in map(chr, range(256)) if not (c.isalnum() or c in [" ", ".", "!", "?", "\\", "/"])) #put allowed characters in the array
def remove_non_alphanumeric(s):
    """Takes markdown string and strips it of its formatting"""

    return s.translate(str.maketrans("","",badchars)).replace("\\n", "\n")
