---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Possible failure to redeem
vuln_class: []
---

# Possible failure to redeem

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** In `Goldivault`, `redeemOwnership()` wouldn't work as expected after calling `changeProtocolParameters/initializeProtocol()` because `endTime/duration` is changed.

**Client:** Acknowledged, we plan to only call changeProtocolParameters after vault has concluded and ownership token holders have had chance to redeem. We will announce that we are going to update parameters and renew.

**Cyfrin:** Acknowledged.
