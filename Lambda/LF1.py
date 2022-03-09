import json
import boto3


def lambda_handler(event, context):
    slot_name = ['Location','Cuisine','NoOfPeople','Date','Time','Email']
    slotToElicit = None
    isFinalSlot = False
    for slot in slot_name:
        if not event['currentIntent']['slots'].get(slot):
            slotToElicit = slot
            break
            
    response = {}
    if slotToElicit:
        response = {
            "dialogAction":{
                "type":"ElicitSlot",
                "intentName":"DiningSuggestionIntent",
                "slotToElicit":slotToElicit,
                "slots":event['currentIntent']['slots']
            }
        }
    else:
        sqs = boto3.client('sqs')
        queue_url = 'https://sqs.us-east-1.amazonaws.com/028437690761/botqueue.fifo'
        msg_body = {
            'Location':event['currentIntent']['slots']['Location'],
            'Cuisine':event['currentIntent']['slots']['Cuisine'],
            'NoOfPeople':event['currentIntent']['slots']['NoOfPeople'],
            'Date':event['currentIntent']['slots']['Date'],
            'Time':event['currentIntent']['slots']['Time'],
            'Email':event['currentIntent']['slots']['Email']
        }
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=0,
            MessageAttributes={
                'Location': {
                    'DataType': 'String',
                    'StringValue': event['currentIntent']['slots']['Location']
                },
                'Cuisine': {
                    'DataType': 'String',
                    'StringValue': event['currentIntent']['slots']['Cuisine']
                },
                'NoOfPeople': {
                    'DataType': 'Number',
                    'StringValue': event['currentIntent']['slots']['NoOfPeople']
                },
                'Date': {
                    'DataType': 'String',
                    'StringValue': event['currentIntent']['slots']['Date']
                },
                'Time': {
                    'DataType':'String',
                    'StringValue': event['currentIntent']['slots']['Time']
                },
                'Email':{
                    'DataType':'String',
                    'StringValue': event['currentIntent']['slots']['Email']
                }
            },
            MessageBody=(
                json.dumps(msg_body)
            ),
            MessageGroupId='groupID'
        )
        response = {
            "dialogAction":{
                "type": "Close",
                "fulfillmentState":"Fulfilled",
                "message": {
                    "contentType":"PlainText",
                    "content": "We have collected the details. The information will be sent to you shortly."
                }
            }
        }
    return response
    
