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

    print('Instances in project %s and zone %s:' % (project, zone))
    for instance in instances:
        print(' - ' + instance['name'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument(
        '--zone',
        default='us-west3-c',
        help='Compute Engine zone to work in.')
    parser.add_argument(
        '--name', default='buba-internal-dev', help='New instance name.')

    args = parser.parse_args()

    main(args.project_id, args.zone, args.name)
# [END run]
