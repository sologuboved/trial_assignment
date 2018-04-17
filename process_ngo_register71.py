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
        for rubric in [TARGETS, ACTIVITIES, PROJECTS, SERVICES, CODES]:
            item = org[rubric]
            if item:
                org[rubric] = str_to_list(item)

    dump_utf_json(orgs, JSON_FNAME)


def str_to_list(string):
    return [item.strip() for item in string.split(DELIMITER) if item]


if __name__ == '__main__':
    # print(str_to_list(u"Развитие волонтерства и добровольчества*+*"))
    dump_orgs()
