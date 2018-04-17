import re
from basic_operations import load_utf_json, dump_utf_json

RAW_JSON_FNAME = 'raw_ngo71.json'
JSON_FNAME = 'ngo71.json'
DELIMITER = '*+*'

TARGETS = 'targets'
ACTIVITIES = 'activities'
PROJECTS = 'projects'
SERVICES = 'services'
CODES = 'codes'
OGRN = 'ogrn'


def dump_orgs():
    orgs = load_utf_json(RAW_JSON_FNAME)
    for org in orgs:
        for rubric in [TARGETS, ACTIVITIES, PROJECTS, SERVICES]:
            item = org[rubric]
            if item:
                org[rubric] = str_to_list(item)
        raw_codes = org[CODES]
        if raw_codes:
            codes = str_to_list(raw_codes)
            org[CODES] = codes
            org[OGRN] = find_ogrn(codes)
        else:
            org[OGRN] = None

    dump_utf_json(orgs, JSON_FNAME)


def str_to_list(string):
    return [item.strip() for item in string.split(DELIMITER) if item]


def find_ogrn(codes):
    for code in codes:
        pattern = r'ОГРН[^0-9]*([0-9]*)'
        try:
            ogrn = re.findall(pattern, code)[0]
        except IndexError:
            continue
        return ogrn


if __name__ == '__main__':
    c = [
      "ИНН:7106042469",
      "Код ОКПО (Росстат):57387361",
      "Код ОКАТО:70401375000"
    ]
    # print(find_ogrn(c))
    dump_orgs()
