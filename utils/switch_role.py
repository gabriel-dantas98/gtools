import boto3

def switching_role(arn, nome):
    sts_client = boto3.client('sts')
    credentials = ""
    try:
        assumedRoleObject = sts_client.assume_role(
            RoleArn=arn,
            RoleSessionName=nome
        )
        credentials = assumedRoleObject['Credentials']
    except Exception as e:
        #Tratamento de erro para caso nao seja possivel realizar o switch role
        print ("Nao foi possivel realizar o switch role {}".format(e))
        credentials = False
    return credentials