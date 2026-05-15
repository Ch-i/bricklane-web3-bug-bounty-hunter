---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Bad design to pull `HONEY` twice from the user
vuln_class: []
---

# Bad design to pull `HONEY` twice from the user

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

Users should approve the transfer twice during the interaction. It would be better to pull the whole amount from the user at a time and transfer to `multisig` from the contract.

```solidity
File: Goldiswap.sol
149:     SafeTransferLib.safeTransferFrom(honey, msg.sender, address(this), price);
150:     SafeTransferLib.safeTransferFrom(honey, msg.sender, multisig, tax);
```
