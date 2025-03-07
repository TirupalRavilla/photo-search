import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
import requests

#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    
    return response

    
def lambda_handler(event, context):
    # TODO implement
    
    
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    client = boto3.client('lex-runtime')
    #logger.debug("In lambda")
    response_lex = client.post_text(
    botName='PhotoSearch',
    botAlias="Prod",
    userId="test",
    inputText= event['q'])
    print("Lex response: ",response_lex)
    if 'slots' in response_lex:
        keys = [response_lex['slots']['searchWord_a'],response_lex['slots']['searchWord']]
        print("Keys: ",keys)
        pictures = search_intent(keys) #get images keys from elastic search labels
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(pictures),
            "isBase64Encoded": False
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": [],
            "isBase64Encoded": False}
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return response
    
# def dispatch(intent_request):
#     #logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
#     intent_name = intent_request['currentIntent']['name']
#     return search_intent(intent_request)

#     raise Exception('Intent with name ' + intent_name + ' not supported')

def search_intent(labels):

    # key1 = get_slots(intent_request)['keyone']
    # key2 = get_slots(intent_request)['keytwo']
    # key3 = get_slots(intent_request)['keythree']
    url = '{{VPC search URL}}'
    #labels = [key1,key2,key3]
    resp = []
    for label in labels:
        if (label is not None) and label != '':
            url2 = url+label
            print("URL: ", url2)
            resp.append(requests.get(url2).json())
    print ("Response: ",resp)
  
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append(key)
   
    #print(url)
    #resp = requests.get(url,headers={"Content-Type": "application/json"}).json()
    #resp = requests.get(url)
    print("Output: ",output)

    return output
