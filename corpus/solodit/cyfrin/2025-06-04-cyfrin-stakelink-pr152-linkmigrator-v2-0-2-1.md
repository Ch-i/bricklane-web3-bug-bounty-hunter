---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0-2-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2-0
title: Inefficient storage layout in `LINKMigrator.Migration`
vuln_class: []
---

# Inefficient storage layout in `LINKMigrator.Migration`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-04-cyfrin-stakelink-pr152-linkmigrator-v2.0.md)_

---

**Description:** Here's the [`LINKMigrator.Migration`](https://github.com/stakedotlink/contracts/blob/0bd5e1eecd866b2077d6887e922c4c5940a6b452/contracts/linkStaking/LINKMigrator.sol#L31-L38) struct:

```solidity
struct Migration {
    // amount of principal staked in Chainlink community pool
    uint128 principalAmount;
    // amount to migrate
    uint128 amount;
    // timestamp when migration was initiated
    uint64 timestamp;
}
```

This struct occupies more than 256 bits and therefore spans two storage slots. However, any LINK amount can be safely stored in a `uint96`, since the total LINK supply is 1 billion (10^9 \* 10^18), which is well below the maximum value representable by a `uint96` (\~7.9 \* 10^28). By changing both amount fields to `uint96`, the struct would comprise `uint96 + uint96 + uint64`, which fits neatly within a single 256-bit storage slot.

**Cyfrin:** Not applicable after fix in [`de672a7`](https://github.com/stakedotlink/contracts/commit/de672a77813d507896502c20241618230af1bd85)

\clearpage
