---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-19
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-20] Refactoring - Roles are not used and could be removed'
vuln_class: []
---

# [L-20] Refactoring - Roles are not used and could be removed

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

Overall roles are used only for `DEFAULT_ADMIN_ROLE` (self) and for `HOT_SIGNER_ROLE` because of this, you could simply remove the roles logic and leave a way to add and remove `HOT_SIGNERS`

https://github.com/solidity-labs-io/kleidi/blob/1a06ac16bc99d0b4081281329d03064c3737f5e4/src/Timelock.sol#L774-L806

```solidity
    function grantRole(bytes32 role, address account)
        public
        override(AccessControl, IAccessControl)
    {
        require(role != DEFAULT_ADMIN_ROLE, "Timelock: cannot grant admin role");
        super.grantRole(role, account);
    }

    /// @notice function to revoke a role from an address
    /// @param role the role to revoke
    /// @param account the address to revoke the role from
    function revokeRole(bytes32 role, address account)
        public
        override(AccessControl, IAccessControl)
    {
        require(
            role != DEFAULT_ADMIN_ROLE, "Timelock: cannot revoke admin role"
        );
        super.revokeRole(role, account);
    }

    /// @notice function to renounce a role
    /// @param role the role to renounce
    /// @param account the address to renounce the role from
    function renounceRole(bytes32 role, address account)
        public
        override(AccessControl, IAccessControl)
    {
        require(
            role != DEFAULT_ADMIN_ROLE, "Timelock: cannot renounce admin role"
        );
        super.renounceRole(role, account);
    }
```

**Mitigation**

Delete the functions

Add a function `grantHotSigner` that requires calling self

If you wish to allow the Safe to also be able to grant hotSigners, you could simply add a role check to `grantHotSigner`
