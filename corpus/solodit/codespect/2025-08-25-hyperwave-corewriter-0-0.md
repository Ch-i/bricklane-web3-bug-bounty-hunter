---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-25-hyperwave-corewriter-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md
tags:
- firm:codespect
- report:2025-08-25-hyperwave-corewriter
title: '[L-01] Blocked whitelist removals for de-listed accounts'
vuln_class: []
---

# [L-01] Blocked whitelist removals for de-listed accounts

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-25-Hyperwave-CoreWriter.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-25-Hyperwave-CoreWriter.md)_

---

**Files:** [`TradeStakeManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/TradeStakeManager.sol#L606), [`VaultManager.sol`](https://github.com/SwellNetwork/hlp-corewriter/blob/5a19bb4373eaf3eb57d872f81d20177fb5cf9b2b/src/VaultManager.sol#L183)

**Description:**

Both `TradeStakeManager` and `VaultManager` maintain separate whitelists to control different operations:

1. `TradeStakeManager` maintains `SpotWhitelist`, `PerpWhitelist`, `ValidatorWhitelist` and `TransferWhitelist`;
2. `VaultManager` maintains `TransferWhitelist` and `VaultWhitelist`;

Those whitelists allow whitelisting of different indexes or addresses per each `HyperCoreAccount` address. It is not possible to update any of those lists without first having the the concrete `HyperCoreAccount` address whitelisted through a separate whitelist - `AccountWhitelist` first. This is also valid for de-listing. Once a `HyperCoreAccount` is de-listed it is not possible to delist anything associated with that account from the above whitelists.

The problem might arise if a `HyperCoreAccount` is de-listed (e.g. due to emergency reasons) and needs to be listed back, yet without certain perps, or indexes, it cannot be done. It must first be whitelisted and only then the perps or indexes can be delisted.

**Impact:** Inability to whitelist an account without previously delisting problematic assets.

**Recommendation:** Allow whitelist removals without checking first if the `HyperCoreAccount` is whitelisted.

**Status:** Fixed

**Client response:** Resolved in [7a406f9e70161ad69884eac8e2f6f4ae84b2cbe1](https://github.com/SwellNetwork/hlp-corewriter/commit/7a406f9e70161ad69884eac8e2f6f4ae84b2cbe1)
