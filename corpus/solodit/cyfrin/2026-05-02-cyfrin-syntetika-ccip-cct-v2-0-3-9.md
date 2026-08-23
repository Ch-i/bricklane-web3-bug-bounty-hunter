---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`TokensHolder::withdraw` discards `transfer` return value and missing event'
vuln_class: []
---

# `TokensHolder::withdraw` discards `transfer` return value and missing event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Uses plain `IERC20.transfer` without checking return value and without `SafeERC20`. The contract has no event for withdrawals. Also `STAKING_VAULT` and `HILBTC` immutable variables lack the `private` visibility marker.

```solidity
issuance/src/helpers/TokensHolder.sol
34:    function withdraw(address to, uint256 amount) external onlyStakingVault {
35:        HILBTC.transfer(to, amount);
36:    }
```

**Recommended Mitigation:** Use `SafeERC20.safeTransfer`, emit `TokensWithdrawn(to, amount)`, and mark the immutables `private` (or expose them deliberately).

**Syntetika:** Fixed in commit [`8662c20`](https://github.com/SyntetikaLabs/monorepo/commit/8662c2004b5b31891a5f7348e0cbf5be87d75d1d)

**Cyfrin:** Verified.
