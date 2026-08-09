---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-dolomite-polvaults-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-dolomite-polvaults-v2-0
title: Missing validation for initialization calldata in `POLIsolationModeWrapperUpgradeableProxy`
  constructor
vuln_class: []
---

# Missing validation for initialization calldata in `POLIsolationModeWrapperUpgradeableProxy` constructor

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-dolomite-POLVaults-v2.0.md)_

---

**Description:** The `POLIsolationModeWrapperUpgradeableProxy` constructor accepts initialization calldata without performing any validation on its content before executing it via `delegatecall` to the implementation contract. Specifically:

- The constructor does not verify that the `calldata` targets the expected initialize(address) function
- The constructor does not verify that the provided vaultFactory address parameter is non-zero

```solidity
// POLIsolationModeWrapperUpgradeableProxy.sol
constructor(
    address _berachainRewardsRegistry,
    bytes memory _initializationCalldata
) {
    BERACHAIN_REWARDS_REGISTRY = IBerachainRewardsRegistry(_berachainRewardsRegistry);
    Address.functionDelegateCall(
        implementation(),
        _initializationCalldata,
        "POLIsolationModeWrapperProxy: Initialization failed"
    );
}
```
This lack of validation means the constructor will blindly execute any calldata, potentially setting critical contract parameters incorrectly during deployment.

Note that a similar issue exists in `POLIsolationModeUnwrapperUpgradeableProxy`


**Impact:** The proxy could be initialized with a zero or invalid vaultFactory address, rendering it non-functional or insecure.  Additionally, if the implementation contract is upgraded and introduces new functions with weaker access controls, this pattern would allow those functions to be called during initialization of new proxies.

**Recommended Mitigation:** Consider adding explicit validation for both the function selector and parameters in the constructor:

```solidity
constructor(
    address _berachainRewardsRegistry,
    bytes memory _initializationCalldata
) {
    BERACHAIN_REWARDS_REGISTRY = IBerachainRewardsRegistry(_berachainRewardsRegistry);

    // Validate function selector is initialize(address)
    require(
        _initializationCalldata.length == 36 &&
        bytes4(_initializationCalldata[0:4]) == bytes4(keccak256("initialize(address)")),
        "Invalid initialization function"
    );

     // Decode and validate the vaultFactory address is non-zero
    address vaultFactory = abi.decode(_initializationCalldata[4:], (address));
    require(vaultFactory != address(0), "Zero vault factory address");

    Address.functionDelegateCall(
        implementation(),
        _initializationCalldata,
        "POLIsolationModeWrapperProxy: Initialization failed"
    );
}
```

**Dolomite:**
Acknowledged.

**Cyfrin:** Acknowledged.
