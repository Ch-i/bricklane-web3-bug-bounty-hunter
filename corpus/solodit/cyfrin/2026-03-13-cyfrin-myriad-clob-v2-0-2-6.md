---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Trader can front run operator causing settlement reverts
vuln_class: []
---

# Trader can front run operator causing settlement reverts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Orders are off-chain signatures only; there is no on-chain lock or escrow of the trader’s collateral or outcome tokens. In `MyriadCTFExchange::_matchOrders` we validate signatures and fill limits, increment `filledAmounts[makerHash]` and `filledAmounts[takerHash]`, and only then call ` MyriadCTFExchange::_settleDirectMatch`, `MyriadCTFExchange::_settleMintMatch`, or `MyriadCTFExchange::_settleMergeMatch`. Those settlement functions pull from the trader via `safeTransferFrom`, collateral in the direct and mint paths, outcome tokens in the merge path. The same pattern holds in `MyriadCTFExchange::matchCrossMarketOrders`: we pull collateral from each buyer after validations and state changes.

Because the pull happens after the on-chain checks and state updates, significant gas will be spent before the revert occurs. The attacker can see the operator's transaction in the mempool, front-run it with a single cheap transfer that moves the required collateral or CTs out of their address, and cause the operator's settlement to revert when `safeTransferFrom` runs. The entire match transaction rolls back, so no state change persists, but the operator has already spent the gas. The griefer only pays for one transfer per grief, and can repeat from many wallets to avoid any blacklisting. And more importantly scale this to many orders costing the protocol gas as well its users timely settlements.

**Impact:** Operators can be repeatedly gas-griefed. Blacklisting addresses does not scale when the griefer uses many wallets and many orders. There is no stake or penalty for causing a revert, so the cost to the griefer is low and the cost to the operator is high.

**Recommended Mitigation:** Consider adding a balance check to the validation portion of the settlement function. Where the balance of each trader needs to be greater than or equal to the cost of the settlement.  This way any revert that would happen would be before the expensive operations and would revert early, reducing the cost to the operator.

Additionally document to operators that simulating transactions is not sufficient and that private mempools should be used to further mitigate these attacks.

**Myriad:** **Cyfrin:**

\clearpage
