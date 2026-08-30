---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Change `v3-rewards/package.json` to require minimum OpenZeppelin v4.9.2 as
  prior versions had a security vulnerability in Merkle Multi Proof
vuln_class: []
---

# Change `v3-rewards/package.json` to require minimum OpenZeppelin v4.9.2 as prior versions had a security vulnerability in Merkle Multi Proof

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** `v3-rewards/package.json` currently [specifies](https://github.com/SolidlyV3/v3-rewards/blob/6dfb435392ffa64652c8f88c98698756ca80cf28/package.json#L7) a minimum OpenZeppelin version of 4.5.0. However some older OZ versions contained a security [vulnerability](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-wprv-93r4-jj2p) in the Merkle Multi Proof which was fixed in 4.9.2.

**Recommended Mitigation:** Change `v3-rewards/package.json` to require minimum OpenZeppelin v4.9.2:
```solidity
"@openzeppelin/contracts": "^4.9.2",
```

**Solidly:**
Fixed in commit [6481747](https://github.com/SolidlyV3/v3-rewards/commit/6481747737b98c8650a36f87b1aeace815505ba9).

**Cyfrin:**
Verified.

\clearpage
