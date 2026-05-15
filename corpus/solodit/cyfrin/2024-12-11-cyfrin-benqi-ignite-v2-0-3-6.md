---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Incorrect revert strings in `StakingContract::revokeAdminRole`
vuln_class: []
---

# Incorrect revert strings in `StakingContract::revokeAdminRole`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** There are two revert strings [[1](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L1021), [2](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L1036)], shown below, in `StakingContract::revokeAdminRole` that appear to have been copied incorrectly and should respectively instead be:
- "Cannot revoke role from the zero address"
- "Attempting to revoke an unrecognized role"

```solidity
function revokeAdminRole(bytes32 role, address account) public {
    // Ensure the account parameter is not a zero address to prevent accidental misassignments
    require(
        account != address(0),
        "Cannot assign role to the zero address"
    );

    /* snip: other conditionals */

    } else {
        // Optionally handle cases where an unknown role is attempted to be granted
        revert("Attempting to grant an unrecognized role");
    }

    /*snip: internal call & event emission */
}
```

**Recommended Mitigation:** Modify the revert strings as suggested.

**BENQI:** Fixed in commits [cd4d43e](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/cd4d43ea8397357b503a127d7ac7966b625a21b7) and [99d7f25](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/commit/99d7f25404a8693f5385d91863b098cd0639bb35).

**Cyfrin:** Verified. The revert strings have been modified.
