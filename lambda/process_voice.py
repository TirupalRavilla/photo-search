import json
from __future__ import print_function
import time
import boto3

def lambda_handler(event, context):
    # TODO implement
    transcribe = boto3.client('transcribe')
    job_name = "job name"
    job_uri = "https://S3 endpoint/test-transcribe/answer2.wav"
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US',
        OutputBucketName='transcription-trr'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(2)
    transcriptionUrl=""
    if status == 'COMPLETED':
        transcriptionUrl= response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(status)
    
    return {
        'statusCode': 200,
        'body': json.dumps(transcriptionUrl)
    }


