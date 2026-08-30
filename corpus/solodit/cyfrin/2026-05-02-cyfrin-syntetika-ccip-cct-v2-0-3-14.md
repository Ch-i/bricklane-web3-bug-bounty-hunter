---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-14
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: 'Cosmetic code cleanups: typo, unused imports, inconsistent types and wrong
  error name'
vuln_class: []
---

# Cosmetic code cleanups: typo, unused imports, inconsistent types and wrong error name

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Grouping of trivial identifier/string cleanups across the codebase. All are non-behavioral and can be fixed mechanically.

---

**1. Typo `PreviousAmoutNotVestedYet` - missing `n`**

Custom error name misspells "Amount".

```solidity
issuance/src/minter/Minter.sol
256:            PreviousAmoutNotVestedYet()
```

Renaming the error is a breaking change for ABIs.

**Recommended:** Rename to `PreviousAmountNotVestedYet`.

---

**2. `HilToken::setMinter` reverts with wrong error name `WaitingPeriodBelowMinimum`**

When the cooldown for a minter change has not elapsed, `setMinter` reverts with `WaitingPeriodBelowMinimum` - the same error used by `updateWaitingPeriod` when the new period is below the minimum. The semantically correct error is `WaitingPeriodNotElapsed` (used identically in `Minter` and for the UUPS upgrade path in `HilToken` itself).

```solidity
issuance/src/token/HilToken.sol
128:        if ($.minter != address(0)) {
129:            require(
130:                $.pendingMinterChange.timestamp + $.requiredWaitingPeriod <=
131:                    block.timestamp,
132:                WaitingPeriodBelowMinimum()
133:            );
134:        }
```

**Recommended:** Replace `WaitingPeriodBelowMinimum()` with `WaitingPeriodNotElapsed()`.

---

**3. Unused imports in `Minter`**

`IERC4626` in `Minter.sol` line 21 is not referenced anywhere in the file.

**Recommended:** Remove the unused imports.

---

**Syntetika:** Fixed in commit [`3d11f17`](https://github.com/SyntetikaLabs/monorepo/commit/3d11f173872177c5922a8ddb53046dffbc99dbb9)

**Cyfrin:** Verified.
