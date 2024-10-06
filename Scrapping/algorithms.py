import re
def string_to_integer(s):
    clean_string = re.sub(r'[^0-9]', '', s)
    return int(clean_string) if clean_string else 0