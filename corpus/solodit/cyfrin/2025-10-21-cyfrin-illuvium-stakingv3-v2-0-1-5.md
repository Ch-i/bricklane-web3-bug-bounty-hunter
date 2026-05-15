---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-1-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Missing `address(0)` check in `setDistributor`
vuln_class: []
---

# Missing `address(0)` check in `setDistributor`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** The `StakingVault::setDistributor` function allows administrators to grant or revoke the DISTRIBUTOR_ROLE to specified accounts, but it lacks validation to prevent assigning this critical role to the zero address (address(0)). While this doesn't create an immediate security vulnerability, it represents an operational risk that could temporarily disrupt the reward distribution mechanism if this is the only address possessing the given role.

**Recommended Mitigation:** Add a zero-address validation check at the beginning of the function:

```solidity
function setDistributor(address account, bool enabled) external onlyRole(ADMIN_ROLE) {
    if (account == address(0)) revert AddressZero("account");

    if (enabled) {
        _grantRole(DISTRIBUTOR_ROLE, account);
    } else {
        _revokeRole(DISTRIBUTOR_ROLE, account);
    }
}
```

**Illuvium:** Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin:** Verified.
