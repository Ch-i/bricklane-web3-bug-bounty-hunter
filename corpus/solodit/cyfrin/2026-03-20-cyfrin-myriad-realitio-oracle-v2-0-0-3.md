---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-20-cyfrin-myriad-realitio-oracle-v2-0-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-20-cyfrin-myriad-realitio-oracle-v2-0
title: Multiple order match front-run gas grief
vuln_class: []
---

# Multiple order match front-run gas grief

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-20-cyfrin-myriad-realitio-oracle-v2.0.md)_

---

**Description:** Orders are off-chain signatures only; no on-chain lock or escrow holds trader collateral or outcome tokens. Settlement pulls from traders via `safeTransferFrom` after validations and state updates, so a front-run that moves collateral or outcome tokens causes a revert after gas is spent. In `matchMultipleOrdersWithFees` the code loops over makers and calls `_matchOrdersSingleValidation` per pair; each call validates, checks balance and allowance, updates `filledAmounts`, then settles.

For example, If the 10th pair has a trader who revoked approval or moved balance, the transaction reverts after the first nine matches have already consumed gas. In `matchCrossMarketOrders` the contract validates all orders in a first loop, then in a second loop for each trader it calls `_checkCollateralBalance` and immediately `safeTransferFrom` in the same iteration. So if the 10th trader front-runs and moves funds, the revert happens after nine check-and-transfer iterations have run; there is no dedicated pass that checks every trader balance and allowance before any transfer. Both paths allow gas griefing, the griefer pays one cheap transfer per grief and the operator loses gas up to the revert. Blacklisting does not scale as this can be done across arbitrary wallets.

**Impact:** Operators are repeatedly gas-griefed. The griefer cost is one transfer per grief; the operator cost is the gas spent up to the revert.

**Recommended Mitigation:** In both `matchMultipleOrdersWithFees` and `matchCrossMarketOrders`, check every trader balance and allowance before the match or transfer loop so any insufficient balance reverts before expensive work. Additionally document that operators should use private mempools.

**ByteStrike:**
We acknowledge this behaviour.
- We'll be the operators running the CLOB and intend to be using a private mempool
- Balance/Allowance checks are done in our API before the order settlement is triggered
- The sorting of the maker orders array can't be determined by an attacker, which therefore creates an unpredictability layer for the attacker
