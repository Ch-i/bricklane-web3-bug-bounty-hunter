---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Insecure Transmission and Handling of Sensitive Information in Interceptor
vuln_class: []
---

# Insecure Transmission and Handling of Sensitive Information in Interceptor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Informational

**Status** : Resolved 

**Description** :  

The httpUtils.js from Interceptor is vulnerable due to the insecure transmission of sensitive information, lack of input validation, and a disregard for secure practices in SSL/TLS certificate validation. These can potentially lead to exposure of sensitive data and Man-In-The-Middle (MITM) attacks.
The application is set to transmit sensitive information such as wallet addresses, encrypted private keys, and API keys without proper SSL/TLS certificate validation (rejectUnauthorized: false). This can expose the communication to interception and manipulation by malicious actors.
There is no validation or sanitation of the inputs provided to the functions. This may leave the application vulnerable to a variety of injection attacks if user-controlled data is passed to these functions.
There is no evident usage of secure headers or proper Content-Type specifications for the requests, which might lead to potential security misconfigurations.

**Recommendation**: 

Enable Strict SSL/TLS Certificate Validation: Do not disable SSL/TLS certificate validation. Always validate certificates properly to ensure the security of the data in transit.
Input Validation and Sanitization: Always validate and sanitize inputs to the functions. Use a proper validation framework or library to ensure that only expected and valid inputs are processed.
#Note : This is used by the interceptor to submit a request to the signing server which is the same Trust boundary as the interceptor (inside an externally restricted VPC).  So above attacks do not apply (and we are doing this for perf reasons since for interception shaving off milliseconds matter).
