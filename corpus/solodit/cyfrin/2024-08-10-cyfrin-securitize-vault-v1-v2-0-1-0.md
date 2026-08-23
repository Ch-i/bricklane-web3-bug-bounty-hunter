---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Unsafe ERC20 Operations should not be used
vuln_class: []
---

# Unsafe ERC20 Operations should not be used

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** In several places, the current implementation uses the function `transfer()` to transfer ERC20 tokens.
```solidity
SecuritizeVault.sol
186: bool success = assetToken.transfer(_to, _transferAmount);
307: bool success = liquidationToken.transfer(msg.sender, assets);
```
But not all ERC20 tokens adhere to the standard. Some tokens do not return boolean and some tokens do not revert on failure.

**Recommended Mitigation:** Use OpenZeppelin's SafeERC20 where the safeTransfer and safeTransferFrom functions handle the return value check as well as non-standard-compliant tokens

**Securitize:** Fix in [3cd6413](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/3cd641372c614587ca3b9f7b6ca850397caa6e5c).

**Cyfrin:** Verified.

\clearpage
