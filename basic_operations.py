import json


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_json(entries, json_file):
    with open(json_file, 'w') as handler:
        json.dump(entries, handler)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)
