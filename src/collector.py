import boto3
import json
import csv
import os
from datetime import datetime

def collect_s3_evidence():
    s3 = boto3.client('s3', region_name='us-east-1')
    evidence = []
    response = s3.list_buckets()
    
    for bucket in response.get('Buckets', []):
        bucket_name = bucket['Name']
        encrypted = False
        try:
            s3.get_bucket_encryption(Bucket=bucket_name)
            encrypted = True
        except Exception:
            encrypted = False
            
        evidence.append({
            "resource_id": bucket_name,
            "resource_type": "AWS::S3::Bucket",
            "control_mapping": "ISO/IEC 27001:2022 A.8.24 / SOC 2 CC6.6",
            "check_description": "Ensure default server-side encryption is enabled",
            "status": "COMPLIANT" if encrypted else "NON_COMPLIANT"
        })
    return evidence

def collect_sg_evidence():
    ec2 = boto3.client('ec2', region_name='us-east-1')
    evidence = []
    sgs = ec2.describe_security_groups()
    
    for sg in sgs.get('SecurityGroups', []):
        sg_id = sg['GroupId']
        has_open_ssh = False
        
        for rule in sg.get('IpPermissions', []):
            if rule.get('FromPort') == 22 or rule.get('ToPort') == 22:
                for ip_range in rule.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        has_open_ssh = True
                        
        evidence.append({
            "resource_id": sg_id,
            "resource_type": "AWS::EC2::SecurityGroup",
            "control_mapping": "NIST SP 800-53 AC-17 / PCI-DSS v4.0 1.3",
            "check_description": "Ensure inbound SSH (Port 22) is restricted from 0.0.0.0/0",
            "status": "NON_COMPLIANT" if has_open_ssh else "COMPLIANT"
        })
    return evidence

def generate_reports(evidence_data):
    os.makedirs('audit_reports', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    json_path = f"audit_reports/evidence_report_{timestamp}.json"
    with open(json_path, 'w') as f:
        json.dump(evidence_data, f, indent=4)
        
    csv_path = f"audit_reports/evidence_report_{timestamp}.csv"
    keys = evidence_data[0].keys() if evidence_data else []
    with open(csv_path, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(evidence_data)
        
    print(f"[+] Audit evidence artifacts generated:\n    - {json_path}\n    - {csv_path}")

if __name__ == "__main__":
    print("[*] Initiating Automated Cloud Compliance Evidence Collection...")
    all_evidence = collect_s3_evidence() + collect_sg_evidence()
    generate_reports(all_evidence)
