---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Minimum deposit value not enforced in `LINKMigrator`
vuln_class: []
---

# Minimum deposit value not enforced in `LINKMigrator`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** The `LINKMigrator` contract includes a `queueDepositMin` field intended to define the minimum deposit amount. However, this value is currently unused, allowing users to deposit amounts as small as 1 juel (1e-18 LINK).

**Impact:** Without enforcement, users can submit deposits smaller than the protocol likely intended, potentially increasing overhead or disrupting expected deposit behavior.

**Recommended Mitigation:** Consider either removing the unused `queueDepositMin` field or enforcing it in the `initiateMigration` function:

```diff
  function initiateMigration(uint256 _amount) external {
-     if (_amount == 0) revert InvalidAmount();
+     if (_amount < queueDepositMin) revert InvalidAmount();
```

**stake.link:**
Fixed in [`0abd4f8`](https://github.com/stakedotlink/contracts/commit/0abd4f86e3c5ed28f9ea444fdc9db5394ad5b5ed)

**Cyfrin:** Verified. `queueDepositMin` is removed. `minStakeAmount` is now fetched from the community pool and verified against `_amount`:
```solidity
(uint256 minStakeAmount, ) = communityPool.getStakerLimits();
if (_amount < minStakeAmount) revert InvalidAmount();
```
