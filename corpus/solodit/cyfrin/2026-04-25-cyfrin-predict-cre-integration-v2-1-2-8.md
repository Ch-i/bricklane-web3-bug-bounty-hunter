---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: 'Code style and naming conventions: inconsistent loops, storage prefixes, magic
  numbers and conflicting names'
vuln_class: []
---

# Code style and naming conventions: inconsistent loops, storage prefixes, magic numbers and conflicting names

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of code-style and naming-convention inconsistencies. All are non-behavioral.

---

**1. Loop style inconsistent between `ChainlinkUpDownAdapter::extend` and `_initialize`**

`extend` uses `for (uint32 i = 1; i <= roundCount; i++) { ts += interval; ... }` (inclusive bound from 1). `_initialize` uses `for (uint32 i; i < roundCount; i++) { ... }` (exclusive bound from 0). Both create `roundCount` rounds; the mixed style is confusing and easy to miscount when refactoring either loop.

**Recommended:** Standardize on `i; i < roundCount; ++i` everywhere.

---

**2. State variable naming - `s_` prefix inconsistency**

`ChainlinkReceiverBase` uses `s_` for private storage (`s_forwarderAddress`, `s_expectedAuthor`, `s_expectedWorkflowName`), but `isWorkflowIdValid` in the same contract does not. `ChainlinkUpDownAdapter` uses no prefix at all.

**Recommended:** Pick one convention and apply across the hierarchy - either drop `s_` from `ChainlinkReceiverBase` or adopt it everywhere.

---

**3. Magic numbers without named constants**

Several magic numbers appear inline: `60` (seconds per minute), `2` (outcome slot count), `3` (DS report version), `1 ether` / `0.5 ether` / `0` outcome discriminators, `62` (metadata length).

**Recommended:** Replace with named constants:

```solidity
uint32 private constant MIN_INTERVAL_SECONDS = 60;
uint8  private constant OUTCOME_SLOT_COUNT   = 2;
uint16 private constant CHAINLINK_REPORT_V3  = 3;
int256 private constant OUTCOME_UP           = 1 ether;
int256 private constant OUTCOME_FLAT         = 0.5 ether;
int256 private constant OUTCOME_DOWN         = 0;
uint256 private constant MIN_METADATA_LENGTH = 62;
```

---

**4. `ChainlinkUpDownAdapter::initialize` function name collides with upgradeable-proxy convention**

`ChainlinkUpDownAdapter::initialize` is the round-series initializer, NOT the upgradeable-proxy `Initializable.initialize`. The contract is not upgradeable. The naming collision confuses integrators and static-analysis tooling that treats `initialize` as the proxy initializer.

**Recommended:** Rename to `initializeRoundSeries` or `createRoundSeries`.

---

**Predict.fun:** Fixed in commit [46ab07e](https://github.com/PredictDotFun/prediction-market/commit/46ab07ea9a7efaaffa4e1e41c30f81597b70849d).

**Cyfrin:** Verified.
