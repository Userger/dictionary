import string
strip_symbs = string.whitespace + "\"'"
def load_settings():
    with open('./settings/settings') as s:
        d = {}
        for line in s:
            if line.lstrip().startswith('#') or not line.strip():
                continue
            setting, value = line.split('=')
            val = tuple(map(lambda w: w.strip(strip_symbs), value.split(',')))
            if len(val) == 1:
                d[setting.strip()] = val[0]
            else:
                d[setting.strip()] = val

        return d

