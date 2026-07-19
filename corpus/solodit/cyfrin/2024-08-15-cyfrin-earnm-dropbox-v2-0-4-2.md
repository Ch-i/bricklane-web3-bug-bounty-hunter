---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove `amountToClaim > 0` check in `DropBox::claimDropBoxes` as previously
  reverted if `amountToClaim == 0`
vuln_class: []
---

# Remove `amountToClaim > 0` check in `DropBox::claimDropBoxes` as previously reverted if `amountToClaim == 0`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Remove `amountToClaim > 0` check in `DropBox::claimDropBoxes` as previously reverted if `amountToClaim == 0`:

```solidity
// [Safety check] In case the amount to claim is 0, revert
if (amountToClaim == 0) revert AmountOfEarnmToClaimIsZero();
// ---------------------------------------------------------------------------------------------

//
//
//
//  Contract Earnm Balance and Safety Checks
// ---------------------------------------------------------------------------------------------
// Get the balance of Earnm ERC20 tokens of the contract
uint256 balance = EARNM.balanceOf(address(this));

// [Safety check] Validate there is more than 0 balance of Earnm ERC20 tokens
// [Safety check] Validate there is enough balance of Earnm ERC20 tokens to claim
// @audit remove `amountToClaim > 0` due to prev check which enforced that
// amountToClaim != 0 and amountToClaim is unsigned so can't be negative
if (!(amountToClaim > 0 && balance > 0 && balance >= amountToClaim)) revert InsufficientEarnmBalance();
```

**Mode:**
Fixed in commit [e6231a7](https://github.com/Earnft/dropbox-smart-contracts/commit/e6231a756a50ac36c9e10076d947dcc16b5696ea).

**Cyfrin:** Verified.
