---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-3-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Missing  `redeem` convenience function in the `StakingVault.sol`
vuln_class: []
---

# Missing  `redeem` convenience function in the `StakingVault.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** `StakingVault.sol` implements a number of convenience functions: `stake(uint256 assets)` ,`unstake(uint256 assets)` and  `mint(uint256 shares)`:

```solidity
function mint(uint256 shares) external returns (uint256) {
        return mint(shares, msg.sender);
    }

    function stake(uint256 assets) external returns (uint256) {
        return deposit(assets, msg.sender);
    }

    function unstake(uint256 assets) external returns (uint256 shares) {
        return withdraw(assets, msg.sender, msg.sender);
    }
```

But it does not have a convenience function for `redeem`, consider adding one such as:
```solidity
function redeem(uint256 shares) external returns (uint256 shares) {
        return redeem(shares, msg.sender, msg.sender);
    }
```

**Syntetika:**
Fixed in commit [1625c09](https://github.com/SyntetikaLabs/monorepo/commit/1625c09f07d8c43c7cfc3b051e12a3a95c26f32d).

**Cyfrin:** Verified.
