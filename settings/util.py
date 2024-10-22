import string
strip_symbs = string.whitespace + "\"'"
def load_settings():
    with open('./settings/settings') as s:
        d = {}
        for line in s:
            setting, value = line.split('=')
            val = tuple(map(lambda w: w.strip(strip_symbs), value.split(',')))
            d[setting.strip()] = val
        return d

