---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-07-05-made-for-gamers-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-07-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md
tags:
- firm:zokyo
- report:2022-07-05-made-for-gamers
title: Burnable token.
vuln_class: []
---

# Burnable token.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-07-05-Made for gamers.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-05-Made%20for%20gamers.md)_

---

**Description**

EXPO.sol and EXPOVO.sol inherit the OZ ERC777 standard token which has a default burn function. Though, the default burnable functionality allows every user to burn their own tokens. Thus in case of big distributions or any hack for a big amount, there is an ability for the malicious user to burn enough tokens to affect the economy of the protocol. Thus verify the usage of the default burn functionality. Burn functionality itself is not a security issue, but it crucial for the protocol, thus it needs to be verified and reflected in the report.

**Recommendation**

Verify the usage of the default burn functionality.

**Re-audit comment**

Resolved.

Post-audit:

The Customer team decided to leave the burn functionality, but set a minimum total supply that it cannot go below
