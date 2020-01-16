import argparse
import os
import time

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

# [START list_instances] - keeping this - might be useful later
#def list_instances(compute, project, zone):
#    result = compute.instances().list(project=project, zone=zone).execute()
#    return result['items'] if 'items' in result else None
# [END list_instances]

# [START get_instance]
def get_instance(compute, project, zone, instance_name):
    result = compute.instances().get(project=project, zone=zone, instance=instance_name).execute()
    return result
# [END get_instance]


# [START start_instance]
def start_instance(compute, project, zone, instance_name):
    return compute.instances().start(project=project, zone=zone, instance=instance_name).execute()
# [END start_instance]

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]


# [START run]
def main(project, zone, instance_name, wait=True):
    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)

    instance = get_instance(compute, project, zone, instance_name)
   

    print('Trying to start Instance %s in project %s and zone %s:' % (instance_name, project, zone))
    
    if instance['status'] == 'RUNNING':
        print('Instance already started - The IP Adress is ' + instance['name'] + ' \n')
        ip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        print(ip)
    else:
        print('**** Starting the instance - please wait a few seconds for the operation to complete ****')
        operation = start_instance(compute, project, zone, instance_name)
        wait_for_operation(compute, project, zone, operation['name'])
        print('Instance is running - Getting IP Adreess')
        instance = get_instance(compute, project, zone, instance_name)
        ip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
        print(ip)


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
