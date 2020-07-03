import json

def JsonLoader(data):
    jsondata = ""
    try:
        jsondata = json.loads(data)
    except:
        print('JSON failed to load')
    return jsondata