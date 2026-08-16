---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Missing call to `_setGlobalWhitelist` in `Minter.sol`
vuln_class: []
---

# Missing call to `_setGlobalWhitelist` in `Minter.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** The `Minter.sol` contract inherits the `Whitelist.sol` abstract contract, which manages access control for the `mint ` and `redeem` functions through the `onlyWhitelisted` modifier:

```solidity
  modifier onlyWhitelisted(address addr) {
        require(isAddressWhitelisted(addr), AddressNotWhitelisted());
        _;
    }

    /// @notice Checks if an address is whitelisted.
    /// @param user The address to check.
    /// @return bool True if the address is whitelisted, false otherwise.
    function isAddressWhitelisted(address user) public view returns (bool) {
        if (manualWhitelist[user] || globalWhitelist) { <-------
            return true;
        }

        return complianceChecker.isCompliant(user);
    }

```

The `onlyWhitelisted` modifier checks the `globalWhitelist` flag. The` StakingVault.sol` contract implements the `setGlobalWhitelist ` function, which is crucial because the `StakingVault.sol` contract expects to use it. However, the `Minter.sol` contract, which mints `HilBTC` (the asset for `StakingVault.sol`), does not implement `setGlobalWhitelist`.

**Impact:** The `StakingVault.sol` contract will not work as expected when `setGlobalWhitelist` is enabled because `setGlobalWhitelist` is not implemented in `Minter.sol`.

**Recommended Mitigation:** Consider implementing `setGlobalWhitelist`  in `minter.sol`:

```solidity
 function setGlobalWhitelist(bool enable) external onlyOwner {
        _setGlobalWhitelist(enable);
    }
```

**Syntetika:**
Fixed in commits [1796e5e](https://github.com/SyntetikaLabs/monorepo/commit/1796e5ec7f50e73e5fc4af32365b936244811217), [86c7b2e](https://github.com/SyntetikaLabs/monorepo/commit/86c7b2e30666f4c6522d48b4f4ed05f5d52238b0) by removing the global whitelist functionality as it was not required by the `Minter` contract, and after the fix for L-4 it is not required at all.

**Cyfrin:** Verified.
