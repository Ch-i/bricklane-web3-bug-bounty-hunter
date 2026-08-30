---
affected_contracts: []
derives_from: []
id: solodit-oxorio-2024-02-06-zunami-protocolv2-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md
tags:
- firm:oxorio
- report:2024-02-06-zunami-protocolv2
title: '[ACKNOWLEDGED] High decimals tokens support in `ZunamiStratBase`'
vuln_class: []
---

# [ACKNOWLEDGED] High decimals tokens support in `ZunamiStratBase`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Oxorio_  
_Source report: [2024-02-06-Zunami ProtocolV2.md](https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2024-02-06-Zunami%20ProtocolV2.md)_

---

##### Location
File | Location | Line
--- | --- | ---
[ZunamiStratBase.sol](https://github.com/ZunamiProtocol/ZunamiProtocolV2/tree/8bc108201bef8c4d341ecd3a29a3b1d975019cec/contracts/strategies/ZunamiStratBase.sol#L23 "/contracts/strategies/ZunamiStratBase.sol") | contract `ZunamiStratBase` | 23

##### Description
In the `ZunamiStratBase` contract, the `tokenDecimalsMultipliers` variable is used to support tokens with fewer than 18 decimals. However, there is no provision to support tokens with more than 18 decimals.

##### Recommendation
We recommend implementing support for tokens with high decimal counts.
