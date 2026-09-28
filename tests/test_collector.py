import pytest
import boto3
from moto import mock_aws
from src.collector import collect_s3_evidence, collect_sg_evidence

@mock_aws
def test_s3_evidence_collection():
    s3 = boto3.client('s3', region_name='us-east-1')
    
    # Create compliant bucket
    s3.create_bucket(Bucket='compliant-audit-bucket')
    s3.put_bucket_encryption(
        Bucket='compliant-audit-bucket',
        ServerSideEncryptionConfiguration={
            'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
        }
    )
    
    # Create non-compliant bucket
    s3.create_bucket(Bucket='non-compliant-audit-bucket')
    
    evidence = collect_s3_evidence()
    assert len(evidence) == 2
    
    compliant_item = next(item for item in evidence if item['resource_id'] == 'compliant-audit-bucket')
    non_compliant_item = next(item for item in evidence if item['resource_id'] == 'non-compliant-audit-bucket')
    
    assert compliant_item['status'] == 'COMPLIANT'
    assert non_compliant_item['status'] == 'NON_COMPLIANT'

@mock_aws
def test_sg_evidence_collection():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    
    # Create security group with open SSH
    sg = ec2.create_security_group(GroupName='open-ssh-sg', Description='Test SG')
    ec2.authorize_security_group_ingress(
        GroupId=sg['GroupId'],
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    )
    
    evidence = collect_sg_evidence()
    assert len(evidence) >= 1
    sg_item = next(item for item in evidence if item['resource_id'] == sg['GroupId'])
    assert sg_item['status'] == 'NON_COMPLIANT'
