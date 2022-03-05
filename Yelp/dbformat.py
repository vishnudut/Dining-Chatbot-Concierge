import json 
import boto3
import time 
import yaml

client = boto3.resource('dynamodb')
table = client.Table('yelp-restaurants')


files = ['American.json','Indian.json','Italian.json','Japanese.json','Korean.json']
for file in files:
    data = yaml.safe_load(open(file))
    c=0
    for record in data:
        db_data = {
            "id": str(record['id']),
            "Name": record['name'].encode('utf-8'),
            "Review_Count":str(record['review_count']),
            "Rating":str(record['rating']),
            "Address":{
                "city":str(record['location']['city']),
                "display_address": record['location']['display_address']
            },
            "inertAtTimeStamp": str(time.time()),
            "Coordinates":{
                "latitude": str(record['coordinates']['latitude']),
                "longitude":str(record['coordinates']['longitude'])
            },
            "zipcode":str(record['location']['zip_code'])

        }
        table.put_item(Item =db_data)
        c+=1
        print("Data upload ",c)
    c=0