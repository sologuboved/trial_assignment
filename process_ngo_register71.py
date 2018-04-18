import re
from basic_operations import load_utf_json, dump_utf_json

RAW_JSON_FNAME = 'raw_ngo71.json'
JSON_FNAME = 'data/ngo71.json'
DELIMITER = '*+*'

SOURCE = 'source'
TARGETS = 'targets'
ACTIVITIES = 'activities'
PROJECTS = 'projects'
SERVICES = 'services'
CODES = 'raw_codes'

OGRN = 'ogrn'
INN = 'inn'
KPP = 'kpp'
OKPO = 'okpo'
OKATO = 'okato'


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
            org[OGRN] = find_code(codes, r'ОГРН')
            org[INN] = find_code(codes, r'ИНН')
            org[KPP] = find_code(codes, r'КПП')
            org[OKPO] = find_code(codes, r'ОКПО')
            org[OKATO] = find_code(codes, r'ОКАТО')
        else:
            org[OGRN], org[INN], org[KPP], org[OKPO], org[OKATO] = None, None, None, None, None
        if org[SOURCE] == 'http://nko71.ru/katalog-nko/nko-po-uslugam/sotsialnaya-pomoshch-i-podderzhka/nasledie.html':
            org[OGRN] = '1097100001129'
        if org[SOURCE] == 'http://nko71.ru/katalog-nko/nko-po-gruppam-naseleniya/zhenshchiny-semi-s-detmi/soyuz-' +\
                'pravoslavnykh-zhenshchin.html':
            org[INN] = '7116511663'
            org[KPP] = '711601001'

    dump_utf_json(orgs, JSON_FNAME)


def str_to_list(string):
    return [item.strip() for item in string.split(DELIMITER) if item]


def find_code(raw_codes, target_code):
    for raw_code in raw_codes:
        pattern = target_code + r'[^0-9]*([0-9]+)'
        try:
            ogrn = re.findall(pattern, raw_code)[0]
        except IndexError:
            continue
        return ogrn


def check_codes():
    ind = 0
    orgs = load_utf_json(JSON_FNAME)
    for org in orgs:
        ind += 1
        print(ind)
        print(org[SOURCE])
        print(OGRN, org[OGRN])
        print(INN, org[INN])
        print(KPP, org[KPP])
        print(OKPO, org[OKPO])
        print(OKATO, org[OKATO])
        print()


if __name__ == '__main__':
    dump_orgs()
    check_codes()
    pass
