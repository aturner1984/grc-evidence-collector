# Automated Cloud Evidence Collector (Python & Boto3)

![Python](https://img.shields.io/badge/Language-Python%203-blue)
![SDK](https://img.shields.io/badge/SDK-Boto3%20%2F%20Moto-orange)
![Framework](https://img.shields.io/badge/Framework-ISO%2027001%3A2022%20%7C%20SOC%202%20%7C%20NIST-green)

## Executive Summary
This project provides an **Automated Cloud Audit Evidence Collector** built in Python using `boto3`. It queries live or mocked cloud API endpoints to evaluate runtime resource configurations against **ISO/IEC 27001:2022**, **SOC 2 Type II**, and **NIST SP 800-53** baselines.

Instead of manually taking screenshots or extracting CSV export files during audit windows, this engine generates time-stamped, machine-readable JSON artifacts and auditor-friendly CSV summaries automatically.

---

## 🏛️ Framework Mapping & Evidence Scope

| Resource Type | Evaluated Configuration | Direct Framework Mandate | Generated Audit Artifact |
| :--- | :--- | :--- | :--- |
| **AWS::S3::Bucket** | Default Server-Side Encryption (AES256/KMS) | **ISO/IEC 27001:2022** A.8.24<br>**SOC 2 Type II** CC6.6<br>**NIST SP 800-53** SC-28 | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |
| **AWS::EC2::SecurityGroup** | Inbound SSH (Port 22) restricted from `0.0.0.0/0` | **NIST SP 800-53** AC-17 / SC-7<br>**PCI-DSS v4.0** Requirement 1.3<br>**ISO/IEC 27001:2022** A.8.20 | `evidence_report_<timestamp>.json`<br>`evidence_report_<timestamp>.csv` |

---

## 🚀 Quick Start & Unit Testing

```bash
# 1. Clone repository & enter directory
git clone [https://github.com/aturner1984/grc-evidence-collector.git](https://github.com/aturner1984/grc-evidence-collector.git)
cd grc-evidence-collector

# 2. Activate virtual environment & install requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Execute unit tests against local Moto AWS mock environment
pytest tests/


