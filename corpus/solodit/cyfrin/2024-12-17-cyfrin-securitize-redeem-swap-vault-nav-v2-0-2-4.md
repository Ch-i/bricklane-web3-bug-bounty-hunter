---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0
title: Share tokens can be transferred
vuln_class: []
---

# Share tokens can be transferred

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2.0.md)_

---

**Description:** The `SecuritizeVault` implements ERC4626's `deposit` function with an additional restriction requiring the depositor to be the same as the receiver (`_msgSender() == receiver`). While this was intended to ensure vault tokens are only owned by the designated investor, this restriction is ineffective since the share tokens implement ERC20 functionality and can be freely transferred after minting.
```solidity
SecuritizeVault.sol
205:     function deposit(uint256 assets, address receiver)
206:         public
207:         override(ERC4626Upgradeable, ISecuritizeVault)
208:         whenNotPaused
209:         onlyRole(OWNER_ROLE)
210:         returns (uint256)
211:     {
212:         require(_msgSender() == receiver, "Sender should be equal than receiver");//@audit-issue not meaningful because share tokens can be transferred
213:         return super.deposit(assets, receiver);
214:     }
215:
```

**Impact:** The restriction provides a false sense of security and creates unnecessary friction for legitimate use cases where a depositor may want to directly deposit to another address, while failing to achieve the intended access control since tokens remain transferable.

**Recommended Mitigation:**
1. Remove the `_msgSender() == receiver` check since it provides no meaningful benefit.
2. If strict ownership control is required, consider:
   - Implementing transfer restrictions on the share tokens
   - Using a non-transferable token standard
   - Adding an allowlist mechanism for valid token holders

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.

\clearpage
