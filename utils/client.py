import boto3 

def getOnlyService(service):
    client = boto3.client(
        service
    )
    return client


def getClientService(credentials, service):
    client = boto3.client(
        service,
        aws_access_key_id = credentials['AccessKeyId'],
        aws_secret_access_key = credentials['SecretAccessKey'],
        aws_session_token = credentials['SessionToken'],
    )
    return client