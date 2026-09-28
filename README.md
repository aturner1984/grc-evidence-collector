# Automated Cloud Evidence Collector (Python & Boto3)

![Python](https://img.shields.io/badge/Language-Python%203.9%2B-blue)
![SDK](https://img.shields.io/badge/SDK-Boto3%20%2F%20Moto-orange)
![Testing](https://img.shields.io/badge/Testing-Pytest-yellowgreen)
![Framework](https://img.shields.io/badge/Framework-ISO%2027001%3A2022%20%7C%20SOC%202%20%7C%20NIST-brightgreen)

## Executive Summary
This project provides an **Automated Cloud Audit Evidence Collector** built in Python using `boto3`. It queries live or mocked cloud API endpoints to evaluate runtime resource configurations against **ISO/IEC 27001:2022**, **SOC 2 Type II**, and **NIST SP 800-53 Rev. 5** baselines.

Instead of relying on manual screenshot capturing or quarterly manual CSV exports during audit windows, this engine automatically generates time-stamped, machine-readable JSON artifacts and auditor-friendly CSV summaries for continuous audit readiness.

---

 ## 🔎 From Evidence to Resolution

The goal of this project is not only to identify security
configuration issues, but to translate technical findings into
actionable GRC outcomes.

Each finding follows a repeatable lifecycle:

AWS Configuration
        ↓
Evidence Collection
        ↓
Security Finding
        ↓
Risk Identification
        ↓
Framework Mapping
        ↓
Path to Resolution
        ↓
Remediation
        ↓
Validation

### Example: Public SSH Exposure

**Finding:**  
An EC2 Security Group allows inbound SSH (TCP/22) from
`0.0.0.0/0`.

**Risk:**  
Public SSH exposure increases the attack surface and allows
connection attempts from any IPv4 address.

**Framework Mapping:**
- NIST SP 800-53: AC-17 / SC-7
- ISO/IEC 27001:2022: A.8.20
- PCI DSS v4.0: Requirement 1.3

**Path to Resolution:**
1. Identify the affected Security Group.
2. Review inbound rules.
3. Remove `0.0.0.0/0` access from TCP port 22.
4. Restrict SSH to an approved administrative IP/CIDR range.
5. Re-run the evidence collector.
   

---

## 🛡️ 1. Control Mapping Matrix

| Resource Type | Evaluated Configuration | Direct Framework Mandate | Governance Objective | Generated Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **AWS::S3::Bucket** | Default Server-Side Encryption (AES256/KMS) | **ISO/IEC 27001:2022** Annex A 8.24<br>**SOC 2 Type II** CC6.6<br>**NIST SP 800-53 Rev. 5** SC-28 | **Data Protection:** Ensure all stored data objects are cryptographically protected at rest by default. | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |
| **AWS::EC2::SecurityGroup** | Inbound SSH (Port 22) restricted from `0.0.0.0/0` | **NIST SP 800-53 Rev. 5** AC-17 / SC-7<br>**PCI-DSS v4.0** Requirement 1.3<br>**ISO/IEC 27001:2022** Annex A 8.20 | **Perimeter Boundary Protection:** Prevent public internet exposure of administrative endpoints. | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |

---

## 🛠️ 2. Tech Stack & Dependencies

* **Language:** Python 3.9+
* **AWS SDK:** `boto3` (v1.34.50) — Used for live cloud API queries against AWS S3 and EC2 services.
* **Mock Engine:** `moto` (v5.0.2) — Used to simulate AWS API responses locally during unit testing without requiring active cloud credentials or incurring AWS costs.
* **Testing Framework:** `pytest` (v8.0.2) — Executes unit test suites verifying evaluation logic and status determination (`COMPLIANT` vs `NON_COMPLIANT`).
* **Artifact Formats:** JSON (machine-readable SIEM/GRC platform ingest) & CSV (auditor sampling workbook).

---

## 🚀 3. Local Reproduction Guide

### Environment Setup & Dependency Installation
```bash
# 1. Clone repository & navigate to root
git clone [https://github.com/aturner1984/grc-evidence-collector.git](https://github.com/aturner1984/grc-evidence-collector.git)
cd grc-evidence-collector

# 2. Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txtpytest tests/
python3 src/collector.py
[ Compliance / Framework Control ]
  ISO/IEC 27001:2022 Annex A 8.24 (Cryptographic Controls)
  SOC 2 CC6.6 (Logical Boundaries & Transmission)
  NIST SP 800-53 Rev. 5 SC-28 (Protection of Information at Rest)
             │
             ▼
[ Governance Objective ]
  Prevent unauthorized data access or disclosure by enforcing cryptographic baselines on cloud storage assets.
             │
             ▼
[ Organizational Policy Definition ]
  All cloud storage repositories (S3 Buckets) storing corporate or customer data must have default server-side encryption enabled.
             │
             ▼
[ Technical Policy Evaluation (`collect_s3_evidence()`) ]
  Boto3 client issues `get_bucket_encryption()` API call against target AWS S3 buckets.
             │
             ▼
[ Audit Finding Classification ]
  ├── Encryption Configured ──► Status marked "COMPLIANT"
  └── Exception Thrown      ──► Status marked "NON_COMPLIANT"
             │
             ▼
[ Audit Evidence Generation ]
  Engine exports time-stamped JSON and CSV evidence artifacts into `audit_reports/` directory for auditor sampling.[*] Initiating Automated Cloud Compliance Evidence Scan...
[*] Querying AWS S3 Buckets in us-east-1...
    - Evaluated: company-audit-logs-prod-001 [COMPLIANT]
    - Evaluated: prod-database-backups-unencrypted-001 [NON_COMPLIANT]
[*] Querying AWS EC2 Security Groups in us-east-1...
    - Evaluated: sg-0a1b2c3d4e5f6g7h8 (open-ssh-sg) [NON_COMPLIANT]

[+] Audit evidence successfully generated:
    - audit_reports/evidence_report_20260928_143000.json
    - audit_reports/evidence_report_20260928_143000.csv
[
    {
        "resource_id": "prod-database-backups-unencrypted-001",
        "resource_type": "AWS::S3::Bucket",
        "control_mapping": "ISO/IEC 27001:2022 A.8.24 / SOC 2 CC6.6",
        "check_description": "Ensure default server-side encryption is enabled",
        "status": "NON_COMPLIANT"
    },
    {
        "resource_id": "company-audit-logs-prod-001",
        "resource_type": "AWS::S3::Bucket",
        "control_mapping": "ISO/IEC 27001:2022 A.8.24 / SOC 2 CC6.6",
        "check_description": "Ensure default server-side encryption is enabled",
        "status": "COMPLIANT"
    },
    {
        "resource_id": "sg-0a1b2c3d4e5f6g7h8",
        "resource_type": "AWS::EC2::SecurityGroup",
        "control_mapping": "NIST SP 800-53 AC-17 / PCI-DSS v4.0 1.3",
        "check_description": "Ensure inbound SSH (Port 22) is restricted from 0.0.0.0/0",
        "status": "NON_COMPLIANT"
    }
]
