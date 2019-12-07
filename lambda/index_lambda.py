import json
import boto3
# from botocore.vendored import requests
import requests
import time
import random


def lambda_handler(event, context):
    
    print("my dog pictures are here")
    
    
    
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    
    
    
    print("bucket name is: " , bucket_name)
    print("key name is:" , key_name)
    
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    resp = client.detect_labels(Image=pass_object)
    
    
    print('<---------Now response object---------->')
    print(json.dumps(resp, indent=4, sort_keys=True))
    
    
    timestamp =time.time()
    #timestamp = event['Records'][0]['eventTime']
    #timestamp = timestamp[:-5]
    labels = []
    #temp = resp['Labels'][0]['Name']
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    print('<------------Now label list----------------->')
    print(labels)
    
    #print('<------------Now required json-------------->')
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    #required_json = json.dumps(format)
    #print(required_json)
    
    print("rekognition ")
    
    
    
    host = "https://vpc-photos-pec7broaqfe7ghfrnfbyoife64.us-east-1.es.amazonaws.com"
    index = "photos"
    type = "dog"
    
    print("index: " , index)
    print("type:" , type)
    
    
    url = host + '/' + index + '/' + type + '/'
    
    
    numr= random.randint(0,99999)
    print("Rand num: ", numr)
    headers = {"Content-Type": "application/json"}
    #url2 = "https://vpc-photos-b4al4b3cnk5jcfbvlrgxxu3vhu.us-east-1.es.amazonaws.com/photos/_search?pretty=true&q=*:*"
    r = requests.post(url + str(numr), data=json.dumps(format).encode("utf-8"), headers=headers)
    #resp_elastic = requests.get(url2,headers={"Content-Type": "application/json"}).json()
    #print('<------------------GET-------------------->')
    #print(r.text)
    #print(json.dumps(resp_elastic, indent=4, sort_keys=True))
    
    print("elastic done")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
