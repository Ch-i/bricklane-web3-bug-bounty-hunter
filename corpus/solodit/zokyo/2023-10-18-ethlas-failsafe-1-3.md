---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-10-18-ethlas-failsafe-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-10-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md
tags:
- firm:zokyo
- report:2023-10-18-ethlas-failsafe
title: Unrestricted Asset Interaction and Lack of Allowlist
vuln_class: []
---

# Unrestricted Asset Interaction and Lack of Allowlist

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-10-18-Ethlas Failsafe.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-10-18-Ethlas%20Failsafe.md)_

---

**Severity** : Informational 

**Status**: Acknowledged  

**Description**:

The service does not impose restrictions or perform validations/sanitizations on the assets it interacts with. Consequently, it creates an exploitable security vulnerability, potentially allowing attackers to exploit the service by using malicious assets, such as a malicious ERC20 token with an overwritten transfer() method. For example, an attacker could mint and drop such a token into a protected account. Since the service does not have an allowlist or validation mechanism, it would perceive such an asset as a legitimate one to protect and potentially interact with it, causing unintended and malicious transactions, leading to account damage.

The impact of this vulnerability is critical as it can lead to unauthorized asset interaction, leading to unintended financial losses, and could potentially compromise the integrity and reputation of the service. It could allow attackers to execute unintended actions like performing maximum approval or even directly drawing funds from a protected account.
Attack Vector:
The attack vector is primarily phishing tokens—tokens specifically crafted with malicious intent, which can perform unauthorized actions when interacted with.
Proof of Concept:
Attacker creates a malicious ERC20 token with a modified transfer() method, which, when called, could trigger unauthorized actions.
Attacker mints and drops this token into a protected account.
The interceptor service, without any allowlist or asset validation, perceives this asset as legitimate and interacts with it.
The malicious transfer() method is triggered, causing unauthorized transactions or actions.

**Recommendation**:

Implement Asset Allowlist: Deploy a strictly managed allowlist of assets that the service is permitted to interact with, preventing interaction with any unauthorized or unverified assets.
Enhance Asset Validation: Develop robust asset validation mechanisms to verify and sanitize the assets before any interaction occurs, reducing the risk of interacting with malicious assets.
