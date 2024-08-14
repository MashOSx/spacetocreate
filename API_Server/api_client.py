import json
import requests # pip install --upgrade requests


## SQLite3 - npcDamageTypes
url = 'http://localhost:12345/api/npc/damage_types/7'
print('URL:  %s' % url)
response = requests.get(url)
print('Status Code:  %s' % response.status_code)
#print(response.text) ## Show payload as text
#print(response.json()) ## Convert payload into JSON object (dict within python)
print(json.dumps(response.json(), indent=4, sort_keys=True))
print('')




## SQLite3 - npcActions
url = 'http://localhost:12345/api/npc/actions/4'
print('URL:  %s' % url)
response = requests.get(url)
print('Status Code:  %s' % response.status_code)
print(json.dumps(response.json(), indent=4, sort_keys=True))
print('')




## MySQL - myapp1.users
url = 'http://localhost:12345/api/users/102'
print('URL:  %s' % url)
response = requests.get(url)
print('Status Code:  %s' % response.status_code)
print(json.dumps(response.json(), indent=4, sort_keys=True))
print('')
