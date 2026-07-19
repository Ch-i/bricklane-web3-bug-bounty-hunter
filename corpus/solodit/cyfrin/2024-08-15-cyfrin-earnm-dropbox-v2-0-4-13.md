---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-13
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
title: Remove redundant `balance > 0` check from `DropBox::claimDropBoxes`
vuln_class: []
---

# Remove redundant `balance > 0` check from `DropBox::claimDropBoxes`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** In `DropBox::claimDropBoxes` there is this check:
```solidity
if (!(balance > 0 && balance >= amountToClaim)) revert InsufficientEarnmBalance();
```

However the `balance > 0` component is redundant since the function already reverted if `amountToClaim == 0`, hence the check can be simplified to:
```solidity
if (!(balance >= amountToClaim)) revert InsufficientEarnmBalance();
```

This can be further simplified by removing the need for the `!` negation operation to:
```solidity
if (balance < amountToClaim) revert InsufficientEarnmBalance();
```

**Mode:**
Fixed in commit [a1e6435](https://github.com/Earnft/dropbox-smart-contracts/commit/a1e6435e922db96194cd74490600e23f8a56e20f).

**Cyfrin:** Verified.
