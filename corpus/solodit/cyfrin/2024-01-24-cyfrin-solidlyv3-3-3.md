---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-3-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md
tags:
- firm:cyfrin
- report:2024-01-24-cyfrin-solidlyv3
title: Cache storage variables in memory when read multiple times without being changed
vuln_class: []
---

# Cache storage variables in memory when read multiple times without being changed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-24-cyfrin-solidlyV3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-24-cyfrin-solidlyV3.md)_

---

**Description:** Cache storage variables in memory when read multiple times without being changed:

File: `SolidlyV3Pool.sol`
```solidity
// @audit no need to load `slot0.fee` twice from storage since it doesn't change;
// load from storage once into memory then use in-memory copy
913:        uint256 fee0 = FullMath.mulDivRoundingUp(amount0, slot0.fee, 1e6);
914:        uint256 fee1 = FullMath.mulDivRoundingUp(amount1, slot0.fee, 1e6);


// @audit `poolFees.token0` and `poolFees.token1` are read from storage multiple times
// but don't get changed until L966 & L971. Load them both from storage once into memory
// then use the in-memory copy instead of repeatedly reading the same value from storage
961:        amount0 = amount0Requested > poolFees.token0 ? poolFees.token0 : amount0Requested;
962:        amount1 = amount1Requested > poolFees.token1 ? poolFees.token1 : amount1Requested;

964:        if (amount0 > 0) {
965:            if (amount0 == poolFees.token0) amount0--; // ensure that the slot is not cleared, for gas savings
966:            poolFees.token0 -= amount0;
967:            TransferHelper.safeTransfer(token0, recipient, amount0);
968:        }
969:        if (amount1 > 0) {
970:            if (amount1 == poolFees.token1) amount1--; // ensure that the slot is not cleared, for gas savings
971:            poolFees.token1 -= amount1;
972:            TransferHelper.safeTransfer(token1, recipient, amount1);
973:        }
```

File: `SolidlyV3Factory.sol`
```solidity
// @audit `owner` is read from storage twice returning the same value each time. Read it from
// storage once into memory, then use the in-memory copy both times
61:        require(msg.sender == owner);
62:        emit OwnerChanged(owner, _owner);
```

**Solidly:**
Acknowledged.
