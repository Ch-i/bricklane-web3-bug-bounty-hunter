---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Overcomplicated `_addPrizes` function designed for incremental updates but
  only used for complete prize resets
vuln_class: []
---

# Overcomplicated `_addPrizes` function designed for incremental updates but only used for complete prize resets

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** The `SpinGame::_addPrizes` function was originally designed to incrementally add new prizes to an existing prize pool while preserving existing prizes. However, the function is only called by `SpinGame::updatePrizes`, which first completely resets the prize state by calling `delete prizeIds` and setting `totalProbabilities = 0`. This makes the preservation logic in `_addPrizes` unnecessary and creates several inefficiencies:

1. The function copies the existing `prizeIds` array into `existingArray`, which is always empty after the reset
2. It creates a new array with size `len + existingArrayLen` where `existingArrayLen` is always 0
3. It loops through the empty existing array to copy non-existent prize IDs

The current implementation effectively replaces the entire prize pool but retains incremental addition logic, left over from a [removed](https://github.com/Consensys/linea-hub/commit/21b48096edbd436311bb4ef688d1b5367c1121ff) `SpinGame::addBatchPrizes` function, which no longer serves a meaningful purpose.

**Impact:** The overcomplicated implementation increases gas costs and code complexity without providing any functional benefit since the incremental addition logic is never utilized.

**Recommended Mitigation:** Since `updatePrizes` always performs a complete reset, we can simplify `_addPrizes` to remove preservation logic and rename it to `_setPrizes`.

**Linea:** Fixed in [PR#558](https://github.com/Consensys/linea-hub/pull/558), commits [`0d8611d`](https://github.com/Consensys/linea-hub/pull/558/commits/0d8611dd06a8c51fe34d1379a2ff7d0bfee1e503), [`f9b1bd2`](https://github.com/Consensys/linea-hub/pull/558/commits/f9b1bd2428dc2d592b182ad99cbf39e18deb6b41), [`e115331`](https://github.com/Consensys/linea-hub/pull/558/commits/e1153312dfdf4851feaf645c2f11efebd5381188), [`2d619e1`](https://github.com/Consensys/linea-hub/pull/558/commits/2d619e104839a017d25e00ba667d340c455f227b), [`7920d00`](https://github.com/Consensys/linea-hub/pull/558/commits/7920d00601ae2c3b31897e62b7faee20bebd271f)

**Cyfrin:** Verified.
* `updatePrizes` renamed to `setPrizes`
* `existingArray` logic removed, no iterating over the previous array.
* delete of `prizeIds` removed, `prizeIds` instead overwritten with the memory array `newPrizeIds`
