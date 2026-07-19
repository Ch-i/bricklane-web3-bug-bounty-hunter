---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Exposure of Sensitive Information
vuln_class: []
---

# Exposure of Sensitive Information

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity**: Low 

**Status** : Resolved 

**Description**: 

In Interceptor the Logger.js having access key ID and secret access key are accessed directly from the configuration, potentially exposing sensitive AWS credentials. Mnemonics, certificates, and secrets are hardcoded in the interceptor/service/conf folder.
Impact: Potential breach or loss of funds if these keys are compromised.

**Recommendation**: 


Store sensitive information using secure environment variables or use AWS IAM Roles and Instance Profiles if running on AWS services like EC2 or Lambda. Use secure vaults or AWS Secrets Manager to store and retrieve sensitive information
