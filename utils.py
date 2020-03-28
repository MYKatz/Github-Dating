#Utility functions

from markdown import Markdown
from io import StringIO


import string

#non-alphanumeric characters
badchars = ''.join(c for c in map(chr, range(256)) if not (c.isalnum() or c in [" ", ".", "!", "?", "\\", "/"])) #put allowed characters in the array
def remove_non_alphanumeric(s):
    """Takes markdown string and strips it of its formatting"""

    return s.translate(str.maketrans("","",badchars)).replace("\\n", "\n")

def form_language_feature_vector(langs):
    """ Create a language feature vector from an array of languages. We """
    print(langs)
    #top 20 most popular programming languages + HTML, CSS
    lang_to_ind = {
        "javascript": 0,
        "python": 1,
        "java": 2,
        "go": 3,
        "c++": 4,
        "ruby": 5,
        "typescript": 6,
        "php": 7,
        "c#": 8,
        "c": 9,
        "shell": 10,
        "scala": 11,
        "rust": 12,
        "swift": 13,
        "dart": 14,
        "kotlin": 15,
        "objective-c": 16,
        "dm": 17,
        "groovy": 18,
        "elixir": 19,
        "html": 20,
        "css": 21
    }

    counts = [0 for _ in range(len(lang_to_ind))]
    total = 0
    for lang in langs:
        if lang and lang.lower() in lang_to_ind:
            counts[lang_to_ind[lang.lower()]] += 1
            total += 1
    
    return [count / total for count in counts]