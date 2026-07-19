---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`ConditionalTokens::redeemVoided` loses dust to rounding, permanently locking
  collateral in `ConditionalTokens`'
vuln_class: []
---

# `ConditionalTokens::redeemVoided` loses dust to rounding, permanently locking collateral in `ConditionalTokens`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `ConditionalTokens::redeemVoided` calculates payouts using integer division by 1e18, which truncates. For positions where `balance * payoutRatio` is not perfectly divisible by 1e18, the remainder is permanently lost in the `ConditionalTokens` contract with no recovery mechanism.

```solidity
// ConditionalTokens.sol:92,98
totalPayout += (outcome0Balance * outcome0Payout) / 1e18;  // truncates
totalPayout += (outcome1Balance * outcome1Payout) / 1e18;  // truncates
```

**Impact:** Dust amounts of collateral are permanently locked in `ConditionalTokens` after voided market redemptions.

**Recommended Mitigation:** The rounding direction correctly favors the protocol however consider adding an admin sweep function for dust. Alternatively, document the rounding behavior.

**Myriad:** Acknowledged. We will properly mention it in our documentation.
