---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-d2-hype-corewriter-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-d2-hype-corewriter-v2-0
title: Unsafe ERC20 transfers
vuln_class: []
---

# Unsafe ERC20 transfers

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-d2-hype-corewriter-v2.0.md)_

---

**Description:** `Hype_Module::hyper_depositSpot` uses `IERC20(token).transfer(...)` directly and ignores the return value. Many ERC-20s are non-standard (e.g., USDT) and either don’t return `bool` or revert on failure in non-obvious ways, making bare `transfer`/`transferFrom` unsafe.

**Impact:** Token transfers can silently fail or behave inconsistently across tokens, causing deposits not to be credited on Core and potentially leaving funds stranded in the caller.

**Recommended mitigation:**
Use OpenZeppelin’s `SafeERC20` for all token interactions:

```solidity
using SafeERC20 for IERC20;

IERC20(token).safeTransfer(assetAddress(uint64(asset)), amount);
```

**D2:** Acknowledged. We're not on mainnet and all tokens most likely use proper compliant ERC20 implementations, so we're skipping on adding SafeERC20 in. We will vet tokens we support in vaults before whitelisting and using.

\clearpage
