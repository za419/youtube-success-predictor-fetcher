import json

with open('output.json') as json_data:
    d = json.load(json_data, strict=False)
    for e in d:
        print e