---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-2-4
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[I-05] Order of calculation in simulateAmountClaimable function'
vuln_class: []
---

# [I-05] Order of calculation in simulateAmountClaimable function

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Original severity:** Best Practices

**Files:** [TokenTableUnlockerV2.sol](https://github.com/EthSign/tokentable-v2-evm/blob/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TokenTableUnlockerV2.sol#L442)

**Description:**

The calculation order in the `simulateAmountClaimable(...)` function can be optimised to reduce precision loss due to integer division. More specifically, the following line:

```solidity
updatedAmountClaimed = (updatedAmountClaimed * actual.totalAmount) / BIPS_PRECISION / TOKEN_PRECISION;
```

Could be changed to this:

```solidity
updatedAmountClaimed = (updatedAmountClaimed * actual.totalAmount) / (BIPS_PRECISION * TOKEN_PRECISION);
```

**Status:** Fixed

**Update from TokenTable:** Fixed in [f2155e0b440808928330ec90aa6003a4c630eb9d](https://github.com/EthSign/tokentable-v2-evm/pull/11/commits/f2155e0b440808928330ec90aa6003a4c630eb9d)
