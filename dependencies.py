import json


def get_data():
    # read json file
    with open("data.json", "r+") as my_file:
        json_data = my_file.read()
        yield (json.loads(json_data), my_file)
