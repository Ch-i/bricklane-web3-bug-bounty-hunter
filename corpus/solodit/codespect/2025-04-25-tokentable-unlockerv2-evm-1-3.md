---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-25-tokentable-unlockerv2-evm-1-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md
tags:
- firm:codespect
- report:2025-04-25-tokentable-unlockerv2-evm
title: '[L-04] defaultFee can be huge or insignificant depending on the project token’s
  decimals'
vuln_class: []
---

# [L-04] defaultFee can be huge or insignificant depending on the project token’s decimals

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-25-TokenTable-UnlockerV2-EVM.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-25-TokenTable-UnlockerV2-EVM.md)_

---

**Files:** [TTUFeeCollector.sol](https://github.com/EthSign/tokentable-v2-evm/tree/e27192f627ea849f88e8a4b68382c5ac8808e3a5/contracts/core/TTUFeeCollector.sol)

**Description:**

Projects can deploy an Unlocker for their project token in a permissionless manner through the deployer. If there is no communication or intervention from the protocol team to set up custom fees for the Unlocker, then the `defaultFee` is charged every time users call the `claim(...)` function. However, this `defaultFee` is a fixed fee amount and not a percentage.

Projects can have tokens with varying decimals, ranging from as low as 2 to as high as 24. It is impossible for a `defaultFee` to exist that can fairly cover all these decimals.

**Impact:** Depending on the project token decimals, the `defaultFee` can be huge or very small, requiring the protocol to step in and set up a custom fee. This removes the permissionless nature of the process for the projects.

**Recommendation:** Instead of having the `defaultFee` as a fixed amount, make it a percentage in BIPS.

**Status:** Acknowledged

**Update from TokenTable:** acknowledged
