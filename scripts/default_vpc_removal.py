"""
Default VPC removal script
"""

import argparse
import logging
import time
import boto3

logger = logging.getLogger(__name__)

def get_regions() -> list:
    """
    Get the list of AWS regions

    """
    boto3_session = boto3.session.Session()
    try:
        ec2_client = boto3_session.client('ec2')
        regions = ec2_client.describe_regions()
        region_list = []
        for region in regions["Regions"]:
            region_list.append(region["RegionName"])
        return region_list
    except Exception as e:
        print(f"Error while trying to get the list of AWS regions: {e}")
        return []


def remove_vpc_attachments(vpc_id: str, session: boto3.session.Session):
    """
    Removes the Internet Gateways attached to a specified VPC

    :param vpc_id: The VPC ID
    :param session: The Boto3 session
    """
    try:
        ec2_resource = session.resource('ec2')
        vpc = ec2_resource.Vpc(vpc_id)

        for subnet in vpc.subnets.all():
            for instance in subnet.instances.all():
                print(f"Terminating instance {instance.id}...")
                response = instance.terminate()
                while response["TerminatingInstances"][0]["CurrentState"]["Name"] != "terminated":
                    print(f"Waiting for instance {instance.id} termination...")
                    time.sleep(5)
                    response = instance.terminate()
        print(f"Successfully terminated the instances attached to the VPC {vpc_id}")

        for igw in vpc.internet_gateways.all():
            print(f"Detaching IGW {igw.id} from {vpc_id}...")
            igw.detach_from_vpc(VpcId=vpc_id)
            print(f"Deleting IGW {igw.id}...")
            igw.delete()
        print(f"Successfully removed the IGWs attached to the VPC {vpc_id}")

        for rt in vpc.route_tables.all():
            for rt_association in rt.associations:
                if not rt_association.main:
                    print(f"Deleting route table association {rt_association.id}...")
                    rt_association.delete()
        print(f"Successfully removed the route table associations attached to the VPC {vpc_id}")

        for sg in vpc.security_groups.all():
            if sg.group_name != "default":
                print(f"Deleting security group {sg.id}...")
                sg.delete()
        print(f"Successfully removed the security groups attached to the VPC {vpc_id}")
        
        for nacl in vpc.network_acls.all():
            if not nacl.is_default:
                print(f"Deleting network ACL {nacl.id}...")
                nacl.delete()
        print(f"Successfully removed the network ACLs attached to the VPC {vpc_id}")

        for subnet in vpc.subnets.all():
            print(f"Deleting subnet {subnet.id}...")
            subnet.delete()
        print(f"Successfully removed the subnets attached to the VPC {vpc_id}")

    except Exception as e:
        print(f"Error while trying to remove the resources attached to the VPC {vpc_id}: {e}")


def remove_default_vpc(region: str):
    """
    Removes the default VPC on an AWS account in a specified region

    :param region: The AWS region in which the default VPC will be removed
    """
    boto3_session = boto3.session.Session(region_name=region)
    try:
        ec2_client = boto3_session.client('ec2')

        default_vpcs = ec2_client.describe_vpcs(
            Filters=[
            {
                'Name' : 'isDefault',
                'Values' : [
                    'true',
                ],
            },
            ]
        )

        default_vpc_ids = []
        for vpc in default_vpcs["Vpcs"]:
            default_vpc_ids.append(vpc["VpcId"])

        for vpc_id in default_vpc_ids:
            print(f"Trying to remove the resources attached to the VPC {vpc_id}...")
            remove_vpc_attachments(vpc_id, boto3_session)
            print(f"Trying to remove the VPC {vpc_id}...")
            ec2_client.delete_vpc(VpcId=vpc_id)
            print(f"Successfully removed the VPC {vpc_id}")

    except Exception as e:
        print(f"Error while trying to remove the default VPC in {region}: {e}")


def remove_default_vpcs():
    """
    Removes the default VPCs on an AWS account

    """
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("Getting the regions list...")
    region_list = get_regions()

    for region in region_list:
        print(f"Trying to remove the default VPC in region {region}...")
        print("--------------------")
        remove_default_vpc(region)
        print("--------------------")


if __name__ == '__main__':
    remove_default_vpcs()
