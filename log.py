import json

def write_json(data):
    json_object = json.dumps(data, indent=4)
   # print(json_object)
    # Writing to sample.json
    with open("log.json", "w") as outfile:
        outfile.write(json_object)

def get_log():
    with open('log.json', 'r') as f:      
      data = json.load(f)     
    return data    

