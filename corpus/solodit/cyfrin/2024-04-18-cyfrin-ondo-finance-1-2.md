---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Transfer tokens before minting shares in `rOUSG::wrap`
vuln_class: []
---

# Transfer tokens before minting shares in `rOUSG::wrap`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `rOUSG::wrap` [L411-413](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/rOUSG.sol#L411-L413) currently mints shares before transferring tokens used to mint those shares:
```solidity
// mint shares
uint256 ousgSharesAmount = _OUSGAmount * OUSG_TO_ROUSG_SHARES_MULTIPLIER;
_mintShares(msg.sender, ousgSharesAmount);

// transfer tokens used to mint the shares
ousg.transferFrom(msg.sender, address(this), _OUSGAmount);
```
A safer coding pattern is to transfer the tokens first then mint the shares.

**Ondo:**
Acknowledged.
