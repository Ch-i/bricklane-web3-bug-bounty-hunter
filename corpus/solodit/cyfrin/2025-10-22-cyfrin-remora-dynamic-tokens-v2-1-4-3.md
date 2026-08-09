---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-4-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-22-cyfrin-remora-dynamic-tokens-v2-1
title: '`TokenBank::setCustodian` should ensure custodian has ADMIN privileges'
vuln_class: []
---

# `TokenBank::setCustodian` should ensure custodian has ADMIN privileges

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-22-cyfrin-remora-dynamic-tokens-v2.1.md)_

---

**Description:** If the `TokenBank::setCustodian` is called and they don't have ADMIN privileges then `TokenBank::removeToken` will revert since the call to `safeTransfer` will indirectly call `CentralToken.transfer` which has this implementation:

```solidity
    function transfer(address to, uint256 amount) public override returns (bool) {
        if (amount == 0) return true;
        _checkAllowedAdmin(to);
        return super.transfer(to, amount);
    }
```

**Impact:** Minimal since admin can always just call `setCustodian` again or give ADMIN privileges to the custodian.

**Recommended Mitigation:** Add one line to `setCustodian`

```solidity
require(allowlist.allowed(newCustodian) && allowlist.isAdmin(newCustodian),
        "Custodian must be allowlist admin");
```

**Remora:** Fixed at commit [a3ae706](https://github.com/remora-projects/remora-dynamic-tokens/commit/a3ae70627dbeb55ac5f9bfeb6ab4a4512703c6c8)

**Cyfrin:** Verified.
