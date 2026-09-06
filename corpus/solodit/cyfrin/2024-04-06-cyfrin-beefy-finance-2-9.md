---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-2-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Some tokens will be stuck in the protocol forever
vuln_class: []
---

# Some tokens will be stuck in the protocol forever

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Due to the shares donated by the first depositor, some tokens will never be able to be withdrawn but will instead be stuck in the protocol forever.

**Impact:** Some tokens will be permanently stuck in the protocol.

**Recommended Mitigation:** Implement an "end-of-life" state for the protocol which:
1) can only be called by the owner when `StrategyPassiveManagerUniswap` is paused and `BeefyVaultConcLiq::totalSupply == MINIMUM_SHARES` (in this state all users have withdrawn and liquidity has been removed)
2) sends all remaining tokens to `StratFeeManagerInitializable::beefyFeeRecipient`
3) puts the protocol into an "end-of-life" state such that no further functions can be executed

**Beefy:**
Fixed in commit [b520517](https://github.com/beefyfinance/experiments/commit/b520517486fa88da062116f6327ee938dd0b4fb4).

**Cyfrin:** Verified.

\clearpage
