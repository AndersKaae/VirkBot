import json

def JsonLoader(data):
    jsondata = ""
    try:
        jsondata = json.loads(data, strict=False)
    except:
        print('JSON failed to load')
    return jsondata