---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: '`WorldLibertyFinancialV3::_electVestingUpdate` hard-codes "not category 1
  → team" and hard-codes magic category numbers'
vuln_class: []
---

# `WorldLibertyFinancialV3::_electVestingUpdate` hard-codes "not category 1 → team" and hard-codes magic category numbers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** The election branch in `WorldLibertyFinancialV3._electVestingUpdate` partitions the entire legacy-user population on the literal `oldCategory == 1`:

```solidity
// WorldLibertyFinancialV3.sol#L85-L96
uint8 oldCategory = REGISTRY.getLegacyUserCategory(_account);
if (oldCategory == 45 || oldCategory == 47) {
    revert ElectionAlreadyPerformed();
}

uint8 newCategory;
if (oldCategory == 1) {
    newCategory = 45;
} else {
    // assert(oldCategory != 1); // To make clear this else branch should cover non category 1 vesting
    newCategory = 47;
}
```

There are two related concerns here:

1. **Magic numbers.** `1`, `45`, and `47` appear as raw literals inside the core election logic. The TypeScript side of the codebase defines `FinalizedVestingCategory.RETAIL = 45` and `FinalizedVestingCategory.TEAM = 47` ([src/wlfi-constants.ts:34](src/wlfi-constants.ts#L34)), but the Solidity side uses bare integers with no in-contract constants, interfaces-level documentation, or even a `uint8 private constant RETAIL_CATEGORY = 45` declaration. Reviewers and future upgraders must cross-reference external files to understand what each literal means. The same literals appear in `IWorldLibertyFinancialV3` and `WorldLibertyFinancialV3` without a shared source of truth.

2. **Two-way partition of every conceivable category.** The `else` branch catches *every* category that is not exactly `1`, `45`, or `47`, and sends those users to team (47). This includes:
   - Legitimate team/advisor/partner buckets (categories 2..20 as enabled in the deploy script).
   - Categories the project has not yet minted (21..44, 46, 48..255).
   - `category = 0` if the registry ever has an entry with `amount != 0` but `category == 0`. `agentBulkInsertLegacyUsers` does not reject `category == 0`:
     ```solidity
     for (uint256 i; i < _users.length; ++i) {
         if (_users[i] == address(0) || _amounts[i] == 0) {
             revert InvalidBulkInsertLegacyUserAtIndex(i);
         }
         ...
         $.legacyUserMap[_users[i]] = LegacyUser({
             amount: uint112(_amounts[i]),
             category: _categories[i],
             isActivated: false
         });
     }
     ```
     and `wlfiSetCategory` does not reject `_category == 0` either. A user ever inserted with `_category == 0`, and subsequently bypass-activated by the owner, would be elected straight to team.

Per the proposal, early supporters are a distinct cohort from founders/team/advisors/partners, so it is likely that the intent is specifically "category 1 = early supporter → retail, everything else in the current retail/team scope → team". But that intent is not expressed defensively: if the registry acquires any category that should not be eligible for team (e.g. a future non-locked cohort, an accidentally-zero category), it is silently mapped to team.

**Impact:** The code works correctly on the expected inputs (categories 1 and 2..20 with team/advisor/partner semantics). The concern is maintainability and defensive behavior for future expansions of the registry and for operator error in bulk-insert.

**Recommended Mitigation:**
- Introduce named constants in the contract (or in `IWorldLibertyFinancialV3`):
  ```solidity
  uint8 private constant EARLY_SUPPORTER_CATEGORY = 1;
  uint8 public constant RETAIL_CATEGORY  = 45;
  uint8 public constant TEAM_CATEGORY    = 47;
  ```
  and replace every literal with the constant. Doing so matches the TypeScript-side `FinalizedVestingCategory` enum and documents the semantics at the call site.
- Make the partition explicit. For example, require that `oldCategory` is a member of a known "team-like" set before mapping to 47:
  ```solidity
  uint8 oldCategory = REGISTRY.getLegacyUserCategory(_account);
  if (oldCategory == RETAIL_CATEGORY || oldCategory == TEAM_CATEGORY) {
      revert ElectionAlreadyPerformed();
  }

  uint8 newCategory;
  if (oldCategory == EARLY_SUPPORTER_CATEGORY) {
      newCategory = RETAIL_CATEGORY;
  } else if (isKnownTeamCategory(oldCategory)) {
      newCategory = TEAM_CATEGORY;
  } else {
      revert UnknownCategory(oldCategory);
  }
  ```
  Where `isKnownTeamCategory` enumerates the exact categories the proposal intends to migrate to team.
- Reject `_category == 0` in `agentBulkInsertLegacyUsers`, `wlfiSetCategory`, `ownerSetCategoryEnabled`, and `ownerSetCategoryTemplate` (see also the related concerns captured in the separate template-percentage note below).

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
