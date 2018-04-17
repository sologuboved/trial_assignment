import re
from basic_operations import load_utf_json, dump_utf_json

RAW_JSON_FNAME = 'raw_ngo71.json'
JSON_FNAME = 'ngo71.json'
DELIMITER = '*+*'

SOURCE = 'source'
TARGETS = 'targets'
ACTIVITIES = 'activities'
PROJECTS = 'projects'
SERVICES = 'services'
CODES = 'raw_codes'
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
        if org[SOURCE] == 'http://nko71.ru/katalog-nko/nko-po-uslugam/sotsialnaya-pomoshch-i-podderzhka/nasledie.html':
            org[OGRN] = '1097100001129'

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


def check_ogrns():
    ind = 0
    orgs = load_utf_json(JSON_FNAME)
    for org in orgs:
        ind += 1
        print(ind)
        print(org[SOURCE])
        print(org[OGRN])
        print()


if __name__ == '__main__':
    dump_orgs()
    check_ogrns()
    pass
