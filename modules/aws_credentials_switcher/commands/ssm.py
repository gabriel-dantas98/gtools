from pprint import pprint
import boto3

client = boto3.client('ec2', region_name="us-east-1")
    
instances = client.describe_instances()['Reservations']

ec2_list = [ instance["InstanceId"] for instance in [ instance_obj['Instances'][0]  for instance_obj in instances ] ]

print(ec2_list, end="\n")

client_ssm = boto3.client('ssm',  region_name="us-east-1")

#response = client.list_inventory_entries()

ssm_inventory = client_ssm.get_inventory()["Entities"]

pprint(ssm_inventory[0]["Id"])
pprint(ssm_inventory[0]["Data"])
#print(client_ssm.describe_instance_associations_status(ec2_list[0]))