import boto3
import re
import os
from datetime import datetime
from json import dump

from config import HOSTS_DIR, HOST_FILENAME


def save_host_data(data, dirname):
    dest = '{}/{}'.format(HOSTS_DIR, dirname)
    if not os.path.exists(dest):
        os.mkdir(dest)
    try:
        with open('{}/{}'.format(dest, HOST_FILENAME), 'w') as jfile:
            dump(data, jfile)
    except OSError:
        return False
    return True


ec2 = boto3.client('ec2')
responses = ec2.describe_instances()['Reservations']

for nr, response in enumerate(responses):
    new_host = {}
    inst = response['Instances'][0]
    tags = inst['Tags']

    new_host['ip'] = inst['PrivateIpAddress']
    new_host['inst_id'] = inst['InstanceId']
    new_host['img_id'] = inst['ImageId']
    new_host['inst_type'] = inst['InstanceType']

    tags_keys = [tag['Key'] for tag in tags]
    if 'Name' in tags_keys:
        new_host['name'] = [tag['Value']
                            for tag in tags if tag['Key'] == 'Name'][0]
    if 'OS' in tags_keys:
        new_host['os'] = [tag['Value']
                          for tag in tags if tag['Key'] == 'OS'][0]
    if 'KeyName' in inst:
        new_host['key'] = inst['KeyName']

    new_host['launch_time'] = datetime.strftime(
        inst['LaunchTime'], "%Y-%m-%d %H:%M:%S")

    print(new_host)
    save_host_data(new_host, new_host['ip'])
