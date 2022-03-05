import requests
import json

client_id = 'RMsG8_CXd4G5qAfChGx2iA'
api_key = '5ZmugUISAT8yh3XfOEhbqClDexZzlvdujkoP1NCfoo0UE95p8g1YaB-Pb_rednvnrmW0EjgqY_Rkb4vbypVzdyUkc_FCdLlhU8Dqm0etSOmgSP2UJpf7raIp5_EdYnYx'
headers = {
    "Authorization" : "Bearer 5ZmugUISAT8yh3XfOEhbqClDexZzlvdujkoP1NCfoo0UE95p8g1YaB-Pb_rednvnrmW0EjgqY_Rkb4vbypVzdyUkc_FCdLlhU8Dqm0etSOmgSP2UJpf7raIp5_EdYnYx"
}
params = {
    "location": "New York City",
    "term":"Indian",
    "limit":50,
    "offset":0,
    "categories":"restaurants"
}

def get_data(params):
    records = []
    for i in range(0,1000,50):
        params["offset"] = i
        response = requests.get("https://api.yelp.com/v3/businesses/search",params=params, headers=headers)
        records.extend(response.json()['businesses'])
    with open(params["term"]+'.json', 'w') as json_file:
        json.dump(records, json_file)


cuisines = ['Indian','Italian','Korean','Japanese','American']
for cuisine in cuisines:
    params['term'] = cuisine
    get_data(params)
    print("Done",cuisine)




#print(response.json())


#print(response.json()['businesses'])
