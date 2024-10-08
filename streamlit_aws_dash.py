import streamlit as st
import boto3
import polars as pl
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

ec2 = boto3.client('ec2')
autoscaling = boto3.client('autoscaling')
elbv2 = boto3.client('elbv2')
local_tz = pytz.timezone('America/Los_Angeles')
VPC_ID = os.environ['VPC_ID']

layout = [{
    'key': 'instances',
    'display': 'Instances',
}, {
    'key': 'launch_templates',
    'display': 'Launch Templates',
}, {
    'key': 'security_groups',
    'display': 'Security Groups',
}, {
    'key': 'subnets',
    'display': 'Subnets',
}, {
    'key': 'autoscaling_groups',
    'display': 'Autoscaling Groups',
}, {
    'key': 'target_groups',
    'display': 'LB Target Groups',
}, {
    'key': 'load_balancers',
    'display': 'Load Balancers',
}, {
    'key': 'listeners',
    'display': 'LB Listeners',
}]


def main():
    st.set_page_config(page_title='AWS Dashboard', layout='wide')

    data = load_data()
    columns = st.columns([3, 1])

    initialize_sections_enabled()

    with columns[0]:
        for section in layout:
            if not st.session_state[f"{section['key']}_enabled"]:
                continue
            st.write(section['display'], data[section['key']])

    with columns[1]:
        st.button('Refresh', on_click=reload_data)

        for section in layout:
            # the "key" arg publishes the checkbox state to the session state, and vice versa
            st.checkbox(
                section['display'],
                key=f"{section['key']}_enabled",
            )


def toggle_section_enabled(section):
    st.write(section)
    enabled_key = section['key'] + '_enabled'
    st.session_state[enabled_key] = not st.session_state[enabled_key]


def reload_data():
    load_data.clear()


def initialize_sections_enabled():
    for section in layout:
        enabled_key = section['key'] + '_enabled'
        if enabled_key not in st.session_state:
            st.session_state[enabled_key] = True


@st.cache_resource
def get_sections_enabled():
    return {section['key']: True for section in layout}


@st.cache_resource
def get_enabled():
    return


@st.cache_resource
def load_data():
    instances = []
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'id': instance['InstanceId'],
                'public ip': instance['PublicIpAddress'],
                'private ip': instance['PrivateIpAddress'],
                'AZ': instance['Placement']['AvailabilityZone'],
            })

    launch_templates = []
    response = ec2.describe_launch_templates()
    for launch_template in response['LaunchTemplates']:
        launch_templates.append({
            'id':
            launch_template['LaunchTemplateId'],
            'name':
            launch_template['LaunchTemplateName'],
            'updated':
            launch_template['CreateTime'].astimezone(local_tz).strftime(
                '%Y-%m-%d %I:%M %p'),
        })

    security_groups = []
    response = ec2.describe_security_groups()
    # st.write(response)
    for security_group in response['SecurityGroups']:
        if security_group['VpcId'] != VPC_ID:
            continue
        security_groups.append({
            'id':
            security_group['GroupId'],
            'name':
            security_group['GroupName'],
            'protocol':
            ','.join(
                set([
                    permission.get('IpProtocol', 'All')
                    for permission in security_group['IpPermissions']
                ])),
            'ports':
            ','.join([
                str(permission.get('ToPort', 'All'))
                for permission in security_group['IpPermissions']
            ]),
        })

    subnets = []
    response = ec2.describe_subnets()
    for subnet in response['Subnets']:
        if subnet['VpcId'] != VPC_ID:
            continue
        subnets.append({
            'id':
            subnet['SubnetId'],
            'name':
            [tag['Value'] for tag in subnet['Tags']
             if tag['Key'] == 'Name'][0],
            'cidr':
            subnet['CidrBlock'],
            'AZ':
            subnet['AvailabilityZone'],
        })

    autoscaling_groups = []
    response = autoscaling.describe_auto_scaling_groups()
    for asg in response['AutoScalingGroups']:
        autoscaling_groups.append({
            'id':
            asg['AutoScalingGroupName'],
            'launch_template':
            asg['LaunchTemplate']['LaunchTemplateName'],
            'min_size':
            asg['MinSize'],
            'max_size':
            asg['MaxSize'],
            'desired_capacity':
            asg['DesiredCapacity'],
        })

    target_groups = []
    response = elbv2.describe_target_groups()
    for target_group in response['TargetGroups']:
        target_groups.append({
            'arn': target_group['TargetGroupArn'],
            'name': target_group['TargetGroupName'],
            'protocol': target_group['Protocol'],
            'port': target_group['Port'],
        })

    load_balancers = []
    response = elbv2.describe_load_balancers()
    for lb in response['LoadBalancers']:
        load_balancers.append({
            'arn': lb['LoadBalancerArn'],
            'name': lb['LoadBalancerName'],
            'type': lb['Type'],
            'dns': lb['DNSName'],
        })

    listeners = []
    for lb_arn in [lb['arn'] for lb in load_balancers]:
        response = elbv2.describe_listeners(LoadBalancerArn=lb_arn)
        for listener in response['Listeners']:
            listeners.append({
                'id':
                listener['ListenerArn'],
                'port':
                listener['Port'],
                'protocol':
                listener['Protocol'],
                'default_action':
                listener['DefaultActions'][0]['Type'],
                'target_group':
                listener['DefaultActions'][0]['TargetGroupArn'],
            })

    data = {}
    data['instances'] = pl.DataFrame(instances)
    data['launch_templates'] = pl.DataFrame(launch_templates)
    data['security_groups'] = pl.DataFrame(security_groups)
    data['subnets'] = pl.DataFrame(subnets)
    data['autoscaling_groups'] = pl.DataFrame(autoscaling_groups)
    data['target_groups'] = pl.DataFrame(target_groups)
    data['load_balancers'] = pl.DataFrame(load_balancers)
    data['listeners'] = pl.DataFrame(listeners)
    return data


if __name__ == '__main__':
    main()
