---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[I-03] transferFundFromVault(...) reverts for a registered strategy whose
  limit is unset or non-numeric'
vuln_class: []
---

# [I-03] transferFundFromVault(...) reverts for a registered strategy whose limit is unset or non-numeric

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountFundManager.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountFundManager.sol), [Configuration.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/Configuration.sol)

**Description:**

`transferFundFromVault(...)` reads the limit as a string with `configuration.getConfiguration(limitKey)` and parses it with `_parseUint`. `getConfiguration(...)` returns an empty string for an unset key, and `_parseUint` reverts with `ParsingFailed()` on an empty or non-numeric string.

**Impact:** A strategy registered through `setStrategyLimitKey(...)` whose `Configuration` value is never set (or set non-numeric) reverts on every `transferFundFromVault` until governance sets a valid number. It only blocks pulls, never allows an over-pull, and is fixed by setting a valid value.

**Recommendation:** Store the limit as a `uint256` per strategy, or validate the resolved value is a non-empty numeric string when the key is set.

**Status:** Acknowledged

**Client response:** The configuration contract is designed for storing all config values of the vault. It’s general, so the value’s type is string. The responsibility of setting the correct value in the configuration contract is of pdao (offchain). We have to set it via Safe, and signers have to verify the data

**CODESPECT fix review:** Acknowledged.
