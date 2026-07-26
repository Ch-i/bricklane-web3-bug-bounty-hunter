---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: '`emergencyCloseRounds` propagates admin-supplied `endPrice` as next round''s
  `startPrice` allowing outcome predetermination'
vuln_class: []
---

# `emergencyCloseRounds` propagates admin-supplied `endPrice` as next round's `startPrice` allowing outcome predetermination

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** `emergencyCloseRounds` (`ChainlinkUpDownAdapter.sol:114-126`) accepts admin-supplied `endPrices` with no validation beyond `endPrice != 0` (`_closeRound:261`). When `_closeRound` executes, it calls `_setNextRoundStartPriceIfPresent` (L289), which writes the `endPrice` as the next round's `startPrice` if that round is pre-created and its price slot is empty (L319: `if (recordedStartPrice == 0)`).

```solidity
        if (present) {
            int192 recordedStartPrice = prices[feedId][startTimestamp];
            if (recordedStartPrice == 0) {
                prices[feedId][startTimestamp] = startPrice;
                recordedStartPrice = startPrice;
            }
            emit ChainlinkUpDownAdapter__RoundStartPriceSet(feedId, interval, startTimestamp, recordedStartPrice);

        }
```

This guard does **not** protect against extreme prices as it only prevents double-writes. The next round's `startPrice` is always `0` before the current round closes (it is set exclusively by the current round's close), so the guard always passes on first write. An admin can supply any extreme price and it propagates unchecked.

**Attack Path:**

```
State: BTC/USD running at ~$78,243
  Round T0: startPrice = 78,243e18 (set at init)
  Round T1: startPrice = 0, pre-created, CTF condition live
  (UP/DOWN tokens for T1 already tradeable on secondary CTF market)

1. Attacker buys UP conditional tokens for Round T1 on secondary market
   before pausing — positions taken while contract is still live

2. Admin pauses contract (PAUSER_ROLE)

3. emergencyCloseRounds(FEED, 300, T0, [1])
   → T0 resolves: 78,243e18 vs 1 → DOWN
   → prices[FEED][T1] = 1  ← T1 startPrice now extreme low
(extreme startPrice visible onchain only AFTER this tx lands and attacker's positions already taken, outcome now locked)

4. Admin unpauses contract

5. CRE closes T1 with real Chainlink price (~78,243e18)
   → T1: startPrice=1 vs endPrice=78,243e18 → UP guaranteed
   → Attacker redeems full T1 pot
```

**Impact:** A holder of `EMERGENCY_CLOSE_ROUND_ROLE` (or a colluder) can predetermine the next round's outcome by supplying an extreme `endPrice` during emergency close.

The attack is not detectable in advance by regular users since the manipulated `startPrice` only becomes visible onchain after the emergency close transaction lands, at which point attacker positions are already taken and the outcome is locked. No remediation path exists for users once the extreme price is written.

It requires admin-level role collusion and contract must be in paused (emergency) state. Real user funds in the next round are at risk if role holders are also market participants making it `low` impact.

**Proof of Concept:**
```
1. Initialize round series with startPrice = 78,243e18
2. Pause contract
3. Emergency close round T0 with endPrice = 1 (1 wei)
4. prices[FEED][T0+300] = 1 (next round's startPrice)
5. CRE closes T0+300 with any real Chainlink price > 1 → outcome = UP guaranteed
```

**Recommended Mitigation:** Do not add a price delta cap, emergency close exists for abnormal conditions (flash crashes, stale feeds, black swan events) where large price moves are legitimate. A delta restriction would break valid emergency use.

Enforce operational separation at the role level:
> Ensure `EMERGENCY_CLOSE_ROUND_ROLE` is held exclusively by a neutral multi-sig with no trading positions. This role must never be held by any entity that participates in the prediction markets, as the emergency price input directly determines subsequent round outcomes. Document this constraint explicitly in deployment runbooks and governance policies.

Alternatively, at the contract level: derive the next round's `startPrice` from an independent onchain oracle snapshot rather than propagating the admin-supplied `endPrice` if possible.

**Predict.fun:** Acknowledge, In the case of emergency, the current time would be X+10 already, so every round from X to X+9's time would already be known offchain, and those markets would be traded towards those outcomes offchain even if not already resolved onchain.

\clearpage
