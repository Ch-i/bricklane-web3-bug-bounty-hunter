---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Fee-on-transfer and rebasing tokens break accounting
vuln_class: []
---

# Fee-on-transfer and rebasing tokens break accounting

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** When recording a bet, the input data is saved directly to storage:
```solidity
function initialize(
    IBet.Bet calldata initialBet,
    string calldata description,
    address pool,
    address treasury
) external initializer {

    _bet = initialBet;
```

This means that the bet amount recorded is the "full" amount, not what was actually received.

**Impact:** Bet cancelled and resolution will revert due to broken accounting, resulting in tokens being locked into the contract.

**Recommended Mitigation:** The easiest solution is to simply not support fee on transfer or rebasing tokens. Otherwise if desiring to support them, tokens should be transferred first then subtract the actual balance from the sent amount to see what was actually received after the fee was deducted, and store that in storage.

For rebasing tokens the mechanism would be similar to how aave balances are handled. Record the total in the contract and split it between maker and taker, for `cancel` and `resolve`. Any left overs can be sent to the `_treasury`.

**WannaBet:** Acknowledged; we decided to not support these and explicitly added a [comment](https://github.com/gskril/wannabet-v2/commit/1fa6da4d2acc96670ad136c733b14c3d2d09e558) to the code.
