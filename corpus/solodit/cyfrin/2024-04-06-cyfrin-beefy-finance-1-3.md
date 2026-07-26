---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Update to `StratFeeManagerInitializable::beefyFeeConfig` retrospectively applies
  new fees to pending LP rewards yet to be claimed
vuln_class: []
---

# Update to `StratFeeManagerInitializable::beefyFeeConfig` retrospectively applies new fees to pending LP rewards yet to be claimed

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** The fee configuration `StratFeeManagerInitializable::beefyFeeConfig` can be updated via `StratFeeManagerInitializable::setBeefyFeeConfig` [L164-167](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/beefy/StratFeeManagerInitializable.sol#L164-L167) while LP rewards are collected and fees charged via `StrategyPassiveManagerUniswap::_harvest` [L306-311](https://github.com/beefyfinance/experiments/blob/14a313b76888581b05d42b6f7b6097c79f3e65c6/contracts/protocol/concliq/uniswap/StrategyPassiveManagerUniswap.sol#L306-L311).

This allows the protocol to enter a state where the fee configuration is updated to for example increase Beefy's protocol fees, then the next time `harvest` is called the higher fees are retrospectively applied to the LP rewards that were pending under the previously lower fee regime.

**Impact:** The protocol owner can retrospectively alter the fee structure to steal pending LP rewards instead of distributing them to protocol users; the retrospective application of fees is unfair on protocol users because those users deposited their liquidity into the protocol and generated LP rewards at the previous fee levels.

**Recommended Mitigation:** 1) `StratFeeManagerInitializable::setBeefyFeeConfig` should be declared virtual
2) `StrategyPassiveManagerUniswap` should override it and before calling the parent function, first call `_claimEarnings` then `_chargeFees`

This ensures that pending LP rewards are collected and have the correct fees charged on them, and only after that has happened is the new fee structure updated.

**Beefy:**
Acknowledged.

\clearpage
