import string
strip_symbs = string.whitespace + "\"'"
def load_settings():
    with open('./settings/settings') as s:
        d = {}
        for line in s:
            if line.lstrip().startswith('#') or not line.strip():
                continue
            setting, value = line.split('=')
            d[setting.strip()] = value.strip(strip_symbs)

        return d


def change_setting(name: str, new_value):
    with open('./settings/settings', 'r') as s:
        lines = s.readlines()
        for i, line in enumerate(lines):
            if line.lstrip().startswith('#') or not line.strip():
                continue
            setting, value = line.split('=')
            if setting.strip() == name:
                new_line = name + '=' + str(new_value).strip('[]()') + '\n'
                lines[i] = new_line
                break

    lines = ''.join(lines)
    with open('./settings/settings', 'w') as s:
        s.write(lines)

