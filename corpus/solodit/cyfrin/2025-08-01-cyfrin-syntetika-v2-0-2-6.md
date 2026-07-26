---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-01-cyfrin-syntetika-v2-0-2-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-01-cyfrin-syntetika-v2-0
title: Owner can not burn tokens from blacklisted addresses
vuln_class: []
---

# Owner can not burn tokens from blacklisted addresses

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-01-cyfrin-syntetika-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md)_

---

**Description:** The `HilBTC.sol` contract contains a logical inconsistency in its `burnFrom()` function regarding blacklisted addresses. While the function grants the `owner` special privileges to burn tokens from any user without requiring allowance (bypassing the `_spendAllowance` check), the underlying `_burn()` function calls `_update()` which contains the `notBlacklisted(from)` modifier. This prevents the owner from burning tokens from blacklisted addresses:
```solidity
 function burnFrom(address from, uint256 amount) external {
        address spender = msg.sender;
        if (spender != from && spender != owner()) {
            _spendAllowance(from, spender, amount);
        }
        _burn(from, amount);
    } //@audit owner can not burn from Blacklisted

    function _update(address from, address to, uint256 amount)
        internal
        override
        notBlacklisted(from)
        notBlacklisted(to)
    {
        super._update(from, to, amount);
    }
```

**Impact:** Owner can not burn tokens from blacklisted addresses.

**Recommended Mitigation:** If you want the owner to have the capability to burn blacklisted user tokens, consider creating a special access control function where the direct `_balances` of the backlisted user is reduced.

**Syntetika:**
Fixed in commit [dc14ad2](https://github.com/SyntetikaLabs/monorepo/commit/dc14ad2c7dacf389deb24fcdca155b5b0acb52d4).

**Cyfrin:** Verified.

\clearpage
