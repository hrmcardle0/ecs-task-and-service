import json
import boto3
import urllib
import os

#initialize cients
ssm_client = boto3.client('ssm')
sns_client = boto3.client('sns')

def handler(event, context):
    # get url to test from parameter-store
    ssm_response = ssm_client.get_parameter(Name='ECSInstanceUrl')
    url = ssm_response["Parameter"]["Value"]
    
    #run tests
    try:
        status_test = getUrlStatus(url)
    except:
        status_test = None
    
    #send to SNS topic
    topic_name = os.environ['SNSTopicName']
    
    #set default message
    message = "An error occured"
    if (status_test):
        message = "Your ECS HTTP container at {} is UP and Running.".format(url)
        print(message)
    else:
        message = "Your ECS HTTP container at {} is DOWN.".format(url)

    sns_response = sns_client.publish(TargetArn=topic_name, Message=message)
    print(sns_response)
    return {
        'statusCode': 200,
        'status': status_test
    }
    
def getUrlStatus(url):
    status_code = urllib.request.urlopen(url, timeout=5).getcode()
    website_is_up = status_code == 200
    return website_is_up