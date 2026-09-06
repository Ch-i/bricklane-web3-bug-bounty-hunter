---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: Missing bounds check on weight values in `WeightedTokensVPCalc` and `WeightedVaultsVPCalc`
vuln_class: []
---

# Missing bounds check on weight values in `WeightedTokensVPCalc` and `WeightedVaultsVPCalc`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** The `WeightedTokensVPCalc` and `WeightedVaultsVPCalc` contracts lack proper bounds checking when setting weight values, which could lead to integer overflow during voting power calculations or complete elimination of voting power through zero weights.

The weight-setting functions in both contracts accept any `uint208` value without validation:

```solidity
// WeightedTokensVPCalc.sol
function setTokenWeight(address token, uint208 weight) public virtual checkPermission {
    _setTokenWeight(token, weight);  // No bounds checking
}

// WeightedVaultsVPCalc.sol
function setVaultWeight(address vault, uint208 weight) public virtual checkPermission {
    _setVaultWeight(vault, weight);  // No bounds checking
}
```

The voting power calculation multiplies stake amounts by these weights without overflow protection:

```solidity
// WeightedTokensVPCalc.sol
function stakeToVotingPower(address vault, uint256 stake, bytes memory extraData)
    public view virtual override returns (uint256) {
    return super.stakeToVotingPower(vault, stake, extraData) * getTokenWeight(_getCollateral(vault)); //@audit could go to 0 or overflow based on weight set
 }
```

**Impact:** Cause an integer overflow (extremely large weight) or total domination of one token over the rest or complete voting power elimination (0 weight).

While the weight-setting functions are protected by the `checkPermission` modifier and controlled by network governance in production deployments, technical safeguards remain important.

**Recommended Mitigation:** Consider implementing a min and max weight that are either constants or immutable.

```solidity
contract WeightedTokensVPCalc is NormalizedTokenDecimalsVPCalc, PermissionManager {
    uint208 public constant MIN_WEIGHT = 1e6;     // Minimum non-zero weight
    uint208 public constant MAX_WEIGHT = 1e18;    // Maximum reasonable weight

    function setTokenWeight(address token, uint208 weight) public virtual checkPermission {
        require(weight <= MAX_WEIGHT, "Weight exceeds maximum");
        require(weight <= MAX_SAFE_WEIGHT, "Weight risks overflow");

        _setTokenWeight(token, weight);
    }
}
```

**Symbiotic:** Fixed in [2a8b18d](https://github.com/symbioticfi/relay-contracts/pull/36/commits/2a8b18d8d6bb8b487b8eecf4485758f1d6fe93a5).

**Cyfrin:** Verified.
