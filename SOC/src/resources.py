import os

from datetime import datetime
from json import dump
from glob import glob
from pathlib import Path
from os.path import isdir
from shutil import rmtree

import boto3

from config import HOSTS_DIR, HOST_FILENAME


def connect():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()['Reservations']
    return response


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


def clear_terminated(hosts):
    hosts_dirs = glob('{}/*/'.format(HOSTS_DIR))
    for host_dir in hosts_dirs:
        host_ip = Path(host_dir).name
        if host_ip in hosts:
            continue
        if isdir(host_dir):
            print('[DEBUG] Removing terminated host from database: {}'.format(host_ip))
            rmtree(host_dir)


def run(dry_run=False):
    response = connect()
    host_list = []

    for response in response:
        # get host specs
        inst = response['Instances'][0]
        tags = inst['Tags']

        # set host info
        new_host = {}
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

        # create host list (by IP)
        host_list.append(new_host['ip'])

        # save data
        if not dry_run:
            save_host_data(new_host, new_host['ip'])

    # clear old data
    if not dry_run:
        clear_terminated(host_list)


if __name__ == '__main__':
    run(True)
