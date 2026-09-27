---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-23-tokentable-ecdsa-distributor-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md
tags:
- firm:codespect
- report:2025-04-23-tokentable-ecdsa-distributor
title: '[I-01] Hook call contains untrusted data'
vuln_class: []
---

# [I-01] Hook call contains untrusted data

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-23-TokenTable-ECDSA-Distributor.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-23-TokenTable-ECDSA-Distributor.md)_

---

**Files:** [BaseECDSADistributor.sol](https://github.com/EthSign/ecdsa-token-distributor/tree/6d5db7f144d7468644313c98f9f310dbaadd1b01/src/core/BaseECDSADistributor.sol), [FungibleTokenWithFeesECDSADistributor.sol](https://github.com/EthSign/ecdsa-token-distributor/tree/6d5db7f144d7468644313c98f9f310dbaadd1b01/src/core/extensions/FungibleTokenWithFeesECDSADistributor.sol)

**Description:**

The `userClaimData` in the hook call is not part of the signed data and is instead allowed to be arbitrarily provided by the caller.

```solidity
function claim(
    ...
    bytes[] calldata extraDatas
)
   ...
{
    //...
}
```

```solidity
function __tryCallClaimHook(...)
    private
{
    address claimHook = _getBaseECDSADistributorStorage().claimHook;
    if (claimHook != address(0)) {
        isBeforeClaim
            ? IClaimHook(claimHook).beforeClaim(delegate, recipient, group, data, extraData)
            : IClaimHook(claimHook).afterClaim(delegate, recipient, group, data, claimedAmount, extraData);
    }
}
```

**Impact:** If the hook incorrectly assumes that this field is trustworthy data, it could impact the system. Moreover, since anyone can claim the receipt on behalf of the user, it’s possible that the input for this field is not what the receipt expected.

**Recommendation:** It is recommended to include this data within the signed data to ensure its trustworthiness.

**Status:** Acknowledged

**Client response:** Acknowledged
