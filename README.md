# Automated Cloud Evidence Collector (Python & Boto3)

![Python](https://img.shields.io/badge/Language-Python%203-blue)
![SDK](https://img.shields.io/badge/SDK-Boto3%20%2F%20Moto-orange)
![Testing](https://img.shields.io/badge/Testing-Pytest-yellowgreen)
![Framework](https://img.shields.io/badge/Framework-ISO%2027001%3A2022%20%7C%20SOC%202%20%7C%20NIST-brightgreen)

## Executive Summary
This project provides an **Automated Cloud Audit Evidence Collector** built in Python using `boto3`. It queries live or mocked cloud API endpoints to evaluate runtime resource configurations against **ISO/IEC 27001:2022**, **SOC 2 Type II**, and **NIST SP 800-53** baselines.

Instead of relying on manual screenshot capturing or quarterly manual CSV exports during audit windows, this engine automatically generates time-stamped, machine-readable JSON artifacts and auditor-friendly CSV summaries.

---

## 🏛️ Control Evaluation & Framework Mapping

> **GRC Engineering Note:** Framework mappings in this project represent illustrative engineering crosswalks demonstrating how automated runtime state evaluations satisfy continuous monitoring controls.

| Resource Type | Evaluated Configuration | Framework Mandate | Control Objective | Generated Artifact |
| :--- | :--- | :--- | :--- | :--- |
| **AWS::S3::Bucket** | Default Server-Side Encryption (AES256/KMS) | **ISO/IEC 27001:2022** A.8.24<br>**SOC 2 Type II** CC6.6<br>**NIST SP 800-53** SC-28 | Cryptographic data-at-rest protection on cloud storage assets. | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |
| **AWS::EC2::SecurityGroup** | Inbound SSH (Port 22) restricted from `0.0.0.0/0` | **NIST SP 800-53** AC-17 / SC-7<br>**PCI-DSS v4.0** Requirement 1.3<br>**ISO/IEC 27001:2022** A.8.20 | Network boundary protection preventing public exposure of administrative ports. | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |

---

## 💻 Interactive Execution & Engine Output

When triggered as part of a scheduled cron job or continuous monitoring workflow, the collector evaluates target cloud API endpoints and outputs real-time scan metrics to `stdout`:

```text
[*] Initiating Automated Cloud Compliance Evidence Scan...
[*] Querying AWS S3 Buckets in us-east-1...
    - Evaluated: company-audit-logs-prod-001 [COMPLIANT]
    - Evaluated: prod-database-backups-unencrypted-001 [NON_COMPLIANT]
[*] Querying AWS EC2 Security Groups in us-east-1...
    - Evaluated: sg-0a1b2c3d4e5f6g7h8 (open-ssh-sg) [NON_COMPLIANT]

[+] Audit evidence successfully generated:
    - audit_reports/evidence_report_20260928_143000.json

