---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary validation of `EnumerableSet` functions
vuln_class: []
---

# Unnecessary validation of `EnumerableSet` functions

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When invoking `EnumerableSet::add` and `EnumerableSet::remove`, it is not necessary to first check whether an element [already exists](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/2f0bc58946db746c0d17a2b9d9a8e13f5a8edd7f/contracts/utils/structs/EnumerableSet.sol#L66) within the set as these functions perform the same validation internally. Instead, the return values should be checked.

Instances include: [`StakingContract::addToken`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L579-595), [`StakingContract::removeToken`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L597-610), [`Ignite::addPaymentToken`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L785-L811), and [`Ignite::removePaymentToken`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L813-L830).

**Recommended Mitigation:** Consider the following diff as an example:

```diff
function addToken(
    address token,
    address priceFeedAddress,
    uint256 maxPriceAge
) external onlyRole(BENQI_ADMIN_ROLE) {
-    require(!acceptedTokens.contains(token), "Token already exists");

    _validateAndSetPriceFeed(token, priceFeedAddress, maxPriceAge);
-    acceptedTokens.add(token);
+    require(acceptedTokens.add(token), "Token already exists");
    emit TokenAdded(token);
}
```

**BENQI:** Fixed in commits [4956824](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/4956824ad9703927c1eab68aa9b2e215cf91f62b) and [420ace6](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/420ace61c598ca1fffc97c9d095b3fe0aafedc97).

**Cyfrin:** Verified. The validation has been updated.
