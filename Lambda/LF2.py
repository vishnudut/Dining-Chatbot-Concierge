import json
import boto3
import requests
import yaml
from random import randrange

client = boto3.resource('dynamodb')
ses_client = boto3.client('ses')
table = client.Table('yelp-restaurants')

host = 'https://search-restaurantdb-2kcj6kxfssnod2fzfpep2qub3e.us-east-1.es.amazonaws.com' # The OpenSearch domain endpoint with https://
index = 'restaurants_index'
url = host + '/' + index 
service = 'es'
headers = { "Content-Type": "application/json" }
auth = ('vishnudut','VvishnuDut1!')


# Create SQS client
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/028437690761/botqueue.fifo'
index_name = 'restaurant_index'
# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
)
print(response)
message = response['Messages'][0]
receipt_handle = message['ReceiptHandle']
sqs.delete_message(
    QueueUrl=queue_url,
    ReceiptHandle=receipt_handle
)

message = json.loads(message['Body'])
q = message['Cuisine']
print(q)

query = {
  # 'size': 5,
  'query': {
    'multi_match': {
      'query': q,
      'fields': ['cuisine']
    }
  }
}
response = requests.get(url+'/_search',auth=auth,headers=headers,data = json.dumps(query))
print(response)

elasticSearchRestaurantData = response.json()['hits']['hits']
length = len(elasticSearchRestaurantData)
dataToRetrieve = elasticSearchRestaurantData[randrange(length)]
print(dataToRetrieve)

output = table.get_item(
  Key = {
    'id':dataToRetrieve['_source']['restaurent_id']
  }
  )
print(output)
mail_body = "Here is your restaurant suggestion:\n" + "Restaurant name: " + output['Item']['Name'] + "\n" + "Restaurant Address: " + (' ').join(output['Item']['Address']['display_address']) + "\n" + "Restaurant rating: " + output['Item']['Rating'] + "\n" + "Review count: " + output['Item']['Review_Count']
print(mail_body)

mail_response = ses_client.send_email(
  Source='vvdut99@gmail.com',
  Destination={
    'ToAddresses':['vvdut99@gmail.com'],
  },
  Message={
    'Subject':{
      'Data':'Restaurant suggestions',
    },
    'Body':{
      'Text':{
        'Data':mail_body,

      }
    }
  }
  
  )
print(mail_response)

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': response.json()
    }
