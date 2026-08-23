---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-1-1
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
title: Reduce approval before transferring tokens in `rOUSG::transferFrom`
vuln_class: []
---

# Reduce approval before transferring tokens in `rOUSG::transferFrom`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `rOUSG::transferFrom` [L286-289](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/rOUSG.sol#L286-L289) currently checks approvals, transfers the tokens then reduces the approvals:
```solidity
// verify approval
require(currentAllowance >= _amount, "TRANSFER_AMOUNT_EXCEEDS_ALLOWANCE");

// perform transfer
_transfer(_sender, _recipient, _amount);

// reduce approval
_approve(_sender, msg.sender, currentAllowance - _amount);
```

A safer coding pattern is to reduce the approval first then transfer tokens similar to OpenZeppelin's [impementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol#L151-L152).

**Ondo:**
Acknowledged.
