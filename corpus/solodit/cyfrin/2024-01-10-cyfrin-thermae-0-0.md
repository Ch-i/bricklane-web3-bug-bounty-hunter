---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-01-10-cyfrin-thermae-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-10T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
tags:
- firm:cyfrin
- report:2024-01-10-cyfrin-thermae
title: On-chain slippage calculation using exchange rate derived from `pool.slot0`
  can be easily manipulated
vuln_class: []
---

# On-chain slippage calculation using exchange rate derived from `pool.slot0` can be easily manipulated

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-01-10-cyfrin-thermae.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md)_

---

**Description:** [On-chain slippage calculation](https://dacian.me/defi-slippage-attacks#heading-on-chain-slippage-calculation-can-be-manipulated) using price from [`pool.slot0` can be easily manipulated](https://solodit.xyz/issues/h-4-no-slippage-protection-during-repayment-due-to-dynamic-slippage-params-and-easily-influenced-slot0-sherlock-real-wagmi-2-git) causing users to receive less tokens than they intended.

**Impact:** Swaps can result in users receiving less tokens than they intended.

**Proof of Concept:** `Portico::calcMinAmount` attempts to on-chain calculate the minimum amount of tokens a swap should return. It does this using:
1) L85 taking as input either the `maxSlippageStart` or `maxSlippageFinish` parameters which users can specify for the 2 possible swaps,
2) L135 getting the current exchange rate on-chain by reading price information from `pool.slot0`

The problem is that [`pool.slot0` is easy to manipulate using flash loans](https://solodit.xyz/issues/h-02-use-of-slot0-to-get-sqrtpricelimitx96-can-lead-to-price-manipulation-code4rena-maia-dao-ecosystem-maia-dao-ecosystem-git) so the actual exchange rate used in the slippage calculation could be far worse than what the user expects; it is very likely users will be continually exploited via sandwich attacks on the swaps.

**Recommended Mitigation:**
1. If price information is required on-chain, use [Uniswap V3 TWAP](https://docs.uniswap.org/concepts/protocol/oracle) instead of `pool.slot0` for more manipulation-resistant price info (note: this does [not offer the same level of protection on Optimism](https://docs.uniswap.org/concepts/protocol/oracle#oracles-integrations-on-layer-2-rollups)),
2. Use `minAmountReceivedStart` and `minAmountReceivedFinish` parameters instead of  `maxSlippageStart` and `maxSlippageFinish` and remove the on-chain slippage calculation. There is no "safe" way to calculate slippage on-chain. If users specify % slippage params, calculate the exact minimum amounts off-chain and pass these in as input.

**Wormhole:**
Fixed in commit af089d6.

**Cyfrin:** Verified.

\clearpage
