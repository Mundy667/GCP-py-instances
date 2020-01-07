import argparse
import os
import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# [START list_instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None
# [END list_instances]

# [START run]
def main(project, zone, instance_name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    instances = list_instances(compute, project, zone)

    print('Starting Instance %s in project %s and zone %s:' % (instance_name, project, zone))

    for instance in instances:
        if instance['name'] == instance_name:
            print(' - IP Adress of ' + instance['name'] + ' \n')
            print(instance['networkInterfaces'][0]['accessConfigs'][0]['natIP'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        '--zone',
        default='europe-west3-c',
        help='Compute Engine zone to work in.')
    parser.add_argument(
        'name', help='the instance name you want to start.')
    args = parser.parse_args()
    main(args.project_id, args.zone, args.name)
# [END run]