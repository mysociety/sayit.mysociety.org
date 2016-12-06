import re

name_fixes = {
}

def title_with_corrections(s):
    s = s.title()
    s = s.replace(' Of ', ' of ').replace(' And ', ' and ').replace('Dac ', 'DAC ') \
         .replace('Qc', 'QC').replace('Ds ', 'DS ')
    # Deal with the McNames
    s = re.sub('Mc[a-z]', lambda mo: mo.group(0)[:-1] + mo.group(0)[-1].upper(), s)
    return s

def fix_name(name):
    name = title_with_corrections(name)
    name = name_fixes.get(name, name)
    # More than one name given, or Lord name that doesn't include full name
    if ' and ' in name or (' of ' in name and ',' not in name):
        return name
    return name
