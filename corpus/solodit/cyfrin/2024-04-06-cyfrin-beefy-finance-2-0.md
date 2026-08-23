---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Missing storage gap in `StratFeeManagerInitializable` can lead to upgrade storage
  slot collision
vuln_class: []
---

# Missing storage gap in `StratFeeManagerInitializable` can lead to upgrade storage slot collision

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** `StratFeeManagerInitializable` is a stateful [upgradeable](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/beefy/StratFeeManagerInitializable.sol#L9) contract with no storage gaps and has [1 child](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L18) with its own state `StrategyPassiveManagerUniswap`.

**Impact:** Should an upgrade occur where the `StratFeeManagerInitializable` contract has additional state added to storage, a storage collision can occur where storage within the child contract `StrategyPassiveManagerUniswap` is overwritten.

**Recommended Mitigation:** Add a storage gap to the `StratFeeManagerInitializable` contract per the OpenZeppelin [documentation](https://docs.openzeppelin.com/upgrades-plugins/1.x/writing-upgradeable#storage-gaps).

**Beefy:**
Fixed in commit [2143322](https://github.com/beefyfinance/experiments/commit/2143322ea2c73a6680675627a0777881cbd4440a).

**Cyfrin:** Verified.
