import re

def tokenize(text):
    return re.findall(pattern=r"(?u)\w+", string=text.lower())