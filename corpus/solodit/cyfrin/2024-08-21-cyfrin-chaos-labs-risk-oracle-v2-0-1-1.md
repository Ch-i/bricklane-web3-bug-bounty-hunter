---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-08-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-21-cyfrin-chaos-labs-risk-oracle-v2-0
title: No restriction on the contract owner becoming an authorized sender
vuln_class: []
---

# No restriction on the contract owner becoming an authorized sender

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-21-cyfrin-chaos-labs-risk-oracle-v2.0.md)_

---

**Description:** Due to the presence of the `onlyOwner` modifier applied to [`RiskOracle::addAuthorizedSender`](https://github.com/ChaosLabsInc/risk-oracle/blob/9449219174e3ee7da9a13a5db7fb566836fb4986/src/RiskOracle.sol#L67-L75), only the contract owner is permitted to add authorized senders. Currently, the only validation present is to prevent adding an authorized sender that is already authorized, so it is possible for the owner to add themselves as an authorized sender. If this is not desired, for example to strictly enforce a separation of concerns between the two roles, then this restriction should be added.

**Chaos Labs:** Acknowledged there is no restriction on the contract owner becoming an authorized sender.

**Cyfrin:** Acknowledged.
