---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-16-cyfrin-ethena-timelock-v2-0-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-05-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-16-cyfrin-ethena-timelock-v2-0
title: Only allow execution if value parameters match `msg.value` to prevent eth remaining
  in the `EthenaTimelockController` contract
vuln_class: []
---

# Only allow execution if value parameters match `msg.value` to prevent eth remaining in the `EthenaTimelockController` contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-16-cyfrin-ethena-timelock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-16-cyfrin-ethena-timelock-v2.0.md)_

---

**Description:** `EthenaTimelockController::execute` and `executeWhitelistedBatch` allow execution without checking that the `msg.value` is equal to the input `value`/`values` parameters.

This can result in eth being temporarily stuck in the contract, though it can be "rescued" by doing a follow-up execution with zero `msg.value` but non-zero `value` input.

**Recommended Mitigation:** Enforce an invariant that the `EthenaTimelockController` should never finish a transaction with a positive ETH balance by:
* in `execute` revert if `msg.value != value`
* in `executeWhitelistedBatch` revert if `msg.value != sum(values)`

The idea being that every execution should use all of the input `msg.value` and no eth from any execution should remain in the `EthenaTimelockController` contract.

**Ethena:** Fixed in commit [89d4190](https://github.com/ethena-labs/timelock-contract/commit/89d41901be3387c11c2150c19eb99883ed807d79) by enforcing this invariant in `execute`, `executeBatch` and `executeWhitelistedBatch`.

**Cyfrin:** Verified.
