---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-02-11-tempest-bridge-oracle-0-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-02-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-02-11-Tempest-Bridge-Oracle.md
tags:
- firm:codespect
- report:2025-02-11-tempest-bridge-oracle
title: '[L-01] GUARDIAN_ROLE is not transferrable'
vuln_class: []
---

# [L-01] GUARDIAN_ROLE is not transferrable

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-02-11-Tempest-Bridge-Oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-02-11-Tempest-Bridge-Oracle.md)_

---

**Files:** [`BridgeOracle.sol`](https://github.com/Tempest-Finance/tempest_smart_contract/blob/f9da49e15ea8f8f66670cb269814c9dd9fde875c/src/utils/BridgeOracle.sol)

**Description:**

The new `GUARDIAN_ROLE` cannot be transferred to other addresses because an admin role for this role hasn’t been set, unlike the `GOVERNANCE_ROLE` which other governors have been allowed to `grantRole` and `revokeRole` from other addresses. As shown below, `_setRoleAdmin(...)` for the `GUARDIAN_ROLE` is missing.

```solidity
constructor(
  address _baseUsdOracle,
  address _quoteUsdOracle,
  address _sequencerUptimeOracle,
  uint64 _baseOracleTimeLimit,
  uint64 _quoteOracleTimeLimit,
  uint64 _sequencerDowntimeLimit,
  bool _isL2,
  string memory _name,
  address governor
) {
  // ...
  _setRoleAdmin(GOVERNANCE_ROLE, GOVERNANCE_ROLE);
  _grantRole(GOVERNANCE_ROLE, governor);
  _grantRole(GUARDIAN_ROLE, governor);
}
```

**Impact:** The `GUARDIAN_ROLE` which is granted to the address, which updates the `isSequencerDown` for L2 networks without a Chainlink Sequencer Uptime Feed, can’t be transferred and is stuck to the initial governor forever.

**Recommendation:** Like the `GOVERNANCE_ROLE`, also set an admin role for the `GUARDIAN_ROLE`.

**Status:** Fixed

**Update from the Tempest:** Fixed in [7af4beaa4d5b011334333e21283eca60f46f9e52](https://github.com/Tempest-Finance/tempest_smart_contract/pull/203/commits/7af4beaa4d5b011334333e21283eca60f46f9e52)
