---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Missing getter function for `SablierBobState::isStakedInAdapter`
vuln_class: []
---

# Missing getter function for `SablierBobState::isStakedInAdapter`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** The `SablierBobState` contract implements getter functionality for all members of the `Vault` struct for a particular `vaultId`. However it does not implement one for the `isStakedInAdapter` member.
```solidity
struct Vault {
        // slot 0
        IERC20 token;
        uint40 expiry;
        uint40 lastSyncedAt;
        // slot 1
        IBobVaultShare shareToken;
        // slot 2
        AggregatorV3Interface oracle;
        // slot 3
        ISablierBobAdapter adapter;
        bool isStakedInAdapter;
        // slot 4
        uint128 targetPrice;
        uint128 lastSyncedPrice;
    }
```

**Recommended Mitigation:** Consider implementing a getter function for the `isStakedInAdapter` member.

**Sablier:** Fixed in commit [c616091](https://github.com/sablier-labs/lockup/pull/1420/changes/c6160910fc7fb6669b11c6338336eab12400dd6d).

**Cyfrin:** Verified.
