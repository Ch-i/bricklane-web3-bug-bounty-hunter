---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use `else if` for sequential `if` statements to prevent subsequent checks when
  a previous check is `true`
vuln_class: []
---

# Use `else if` for sequential `if` statements to prevent subsequent checks when a previous check is `true`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Use `else if` for sequential `if` statements to prevent subsequent checks when a previous check is `true`. For example `DropBoxFractalProtocol::_determineTier` has this code:
```solidity
if (tierId == 6) maxBoxesPerTier = TIER_6_MAX_BOXES;
if (tierId == 5) maxBoxesPerTier = TIER_5_MAX_BOXES;
if (tierId == 4) maxBoxesPerTier = TIER_4_MAX_BOXES;
if (tierId == 3) maxBoxesPerTier = TIER_3_MAX_BOXES;
if (tierId == 2) maxBoxesPerTier = TIER_2_MAX_BOXES;
if (tierId == 1) maxBoxesPerTier = TIER_1_MAX_BOXES;
```

Here even if the first condition is true, all the other `if` statements will still be executed even though they can't be true. Refactor to:
```solidity
if (tierId == 6) maxBoxesPerTier = TIER_6_MAX_BOXES;
else if (tierId == 5) maxBoxesPerTier = TIER_5_MAX_BOXES;
else if (tierId == 4) maxBoxesPerTier = TIER_4_MAX_BOXES;
else if (tierId == 3) maxBoxesPerTier = TIER_3_MAX_BOXES;
else if (tierId == 2) maxBoxesPerTier = TIER_2_MAX_BOXES;
else if (tierId == 1) maxBoxesPerTier = TIER_1_MAX_BOXES;
```

The same issue also applies in a second loop in the same function though the ordering of checks is different and to `DropBoxFractalProtocol::_calculateAmountToClaim`.

**Mode:**
Fixed in commit [fc8466e](https://github.com/Earnft/dropbox-smart-contracts/commit/fc8466edb470680ef7b7606ca34cdda444d18f33).

**Cyfrin:** Verified.
