---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-4-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Use the already-snapshotted list length while compacting claim lists
vuln_class: []
---

# Use the already-snapshotted list length while compacting claim lists

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** Both claim-compaction helpers cache the original list length for their scan, but their subsequent pop loops re-read `genIds.length` from storage for every iteration. Count down from the cached length, or from `len - writeIdx`, to avoid the redundant warm storage read for each removed generation.

```solidity
contracts/AsyncFundVault.sol
855:        uint256[] storage genIds = $.controllerDepositGenerations[controller];
856:        uint256 len = genIds.length;
870:        while (genIds.length > writeIdx) genIds.pop();
913:        uint256[] storage genIds = $.controllerRedeemGenerations[controller];
914:        uint256 len = genIds.length;
933:        while (genIds.length > writeIdx) genIds.pop();
```

**Recommended Mitigation:** In both compaction helpers in `contracts/AsyncFundVault.sol`, use a memory counter for the number of entries to remove. `pop` still performs its required storage update, but the loop predicate no longer needs an additional storage read:

```solidity
for (uint256 remaining = len - writeIdx; remaining != 0; --remaining) {
    genIds.pop();
}
```

**Securitize:** Acknowledged.
