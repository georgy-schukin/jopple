import json


def read_file(file_name):
    with open(file_name, "r") as f:
        return f.read()


def write_file(file_name, data):
    with open(file_name, "w") as f:
        f.write(data)


def read_json(file_name):
    with open(file_name, "r") as f:
        return json.load(f)


def write_json(file_name, json_obj):
    with open(file_name, "w") as f:
        json.dump(json_obj, f, indent=4)


