---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Unnecessary modifier
vuln_class: []
---

# Unnecessary modifier

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** The function `redeem()` has a modifier `receiverSenderNotEqual(_owner)` and it ensures that the caller is actually the owner of the shares.
But this modifier is unnecessary here because it is checked in the `ERC4626::_withdraw()` function.
```solidity
openzeppelin-contracts-upgradeable\contracts\token\ERC20\extensions\ERC4626Upgradeable.sol
291:         ERC4626Storage storage $ = _getERC4626Storage();
292:         if (caller != owner) {
293:             _spendAllowance(owner, caller, shares);
294:         }
```

**Securitize:** Modifier deleted in [52350aa](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/52350aa809c140edc6f794baabc7e53891b37852).

**Cyfrin:** Verified.

\clearpage
