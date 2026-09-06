---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Protocol will leak value to users due to rounding in `SecuritizeSwap::buy`
vuln_class: []
---

# Protocol will leak value to users due to rounding in `SecuritizeSwap::buy`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Protocols should always round against users in favor of the protocol. The `buy` function in the `SecuritizeSwap.sol` is rounding the stable coin need it in favor of the user:

```solidity
 function buy(uint256 _dsTokenAmount, uint256 _maxStableCoinAmount) public override whenNotPaused {
        ...
        uint256 stableCoinAmount = calculateStableCoinAmount(_dsTokenAmount); <----
        dsToken.issueTokensCustom(msg.sender, _dsTokenAmount, block.timestamp, 0, "", 0);

        emit Buy(msg.sender, _dsTokenAmount, stableCoinAmount, navProvider.rate());
    }

  function calculateStableCoinAmount(uint256 _dsTokenAmount) public view returns (uint256) {
        return _dsTokenAmount * navProvider.rate() / (10 ** ERC20(address(dsToken)).decimals()); // rounding down
    }

```

With this rounding down, in theory a user could be minting free DSTokens. However, since the DSToken has only 2 decimals, this is not possible.

**Impact:** The rounding helps users in both directions:

* When depositing: Users might get 1 extra share
* When withdrawing: Users might get 1 extra token

Over thousands of transactions, these wei-level losses accumulate.

**Recommended Mitigation:** Rounding should always favor the protocol; use [`Math::mulDiv`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L280-L282) which supports specifying rounding direction.

**Securitize:** `SecuritizeSwap` was deleted as it is obsolete.

**Cyfrin:** Verified.
