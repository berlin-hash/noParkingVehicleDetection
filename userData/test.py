import json


with open('data.json', 'r') as f:
    dataJson = json.load(f)
    
dict_list = [item for item in dataJson]

for item in dict_list:
    print(item.get('AP29A03839'))