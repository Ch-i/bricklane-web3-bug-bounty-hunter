---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Deprecated `testFail` Usage in Tests
vuln_class: []
---

# Deprecated `testFail` Usage in Tests

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** Several tests ([1](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarket.t.sol#L691-L698), [2](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L236-L248), [3](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L284-L296), [4](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L324-L338), [5](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L369-L382), [6](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L384-L399), [7](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L425-L458), [8](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L596-L633), [9](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L680-L713), [10](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/test/PredictionMarketManager.t.sol#L879-L892)) in `PredictionMarket.t.sol` and `PredictionMarketManager.t.sol` use Foundry’s `testFail` pattern. This pattern has been [deprecated](https://github.com/foundry-rs/foundry/issues/4437) and should be avoided in favor of more explicit revert expectations.

Instead, tests should use `vm.expectRevert()` immediately before the line expected to revert. Ideally, this should include the specific error message to improve clarity and precision: `vm.expectRevert("expected error")`.

Additionally, consider renaming these tests to align with [Foundry's best practices](https://getfoundry.sh/guides/best-practices/writing-tests#organizing-and-naming-tests), using the `test_Revert[When|If]...` format to clearly convey the revert condition.

**Myriad:** Fixed in [PR#89](https://github.com/Polkamarkets/polkamarkets-js/pull/89), commit [`dbcfdfa`](https://github.com/Polkamarkets/polkamarkets-js/pull/89/commits/dbcfdfabe1300fa9629fd227bfac7d02428c231e)

**Cyfrin:** Verified. Tests now catch the expected reverts.
