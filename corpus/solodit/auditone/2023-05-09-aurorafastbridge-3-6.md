---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Limitations and Risks for Users in the Fast Bridge Project Severity: Quality
  Assurance'
vuln_class: []
---

# Limitations and Risks for Users in the Fast Bridge Project Severity: Quality Assurance

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:** 

The Fast Bridge project allows for the transfer of tokens between the NEAR Protocol and Ethereum networks. However, there are several limitations and risks for users. For example, if there is no relayer available to handle the transaction, the tokens will be locked until the valid\_till time, and users will need to contact support to unlock stuck tokens on NEAR. The transaction size is limited by relayer liquidity, and only tokens from the whitelist can be transferred. Additionally, the price is significantly higher than the original bridge.

On the other hand, The Fast Bridge project relies on LP-Relayers to hold locked tokens on the Ethereum side and release them on the NEAR side. However, there are several risks and limitations for relayers. For example, there is a risk of double unlock if the relayer already transferred tokens on the Ethereum side and switches off for a while. The relayer is an off-chain part that needs extra maintenance, including increasing liquidity and key management protection. The relayer can also have issues with the internet or server uptime.

**Recommendations:**

To mitigate these risks, it is recommended ![ref5]that the Fast Bridge project implement a more decentralized approach that reduces reliance on the relayer and provides greater flexibility and scalability for users.
