---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: SharesCooldown Merges Redemption Requests, Making Them Indivisible for Cancel
  and Early Exit
vuln_class: []
---

# SharesCooldown Merges Redemption Requests, Making Them Indivisible for Cancel and Early Exit

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** `SharesCooldown` merges multiple redemption requests into a single request entry when:

1. the user exceeds `MAX_ACTIVE_REQUEST_SLOTS`

2. two requests(last one and current) have the same `unlockAt` (e.g., created in the same block).

```solidity
if (requestsCount < MAX_ACTIVE_REQUEST_SLOTS) {
            if (
                requestsCount > 0 &&
                requests[requestsCount - 1].unlockAt == unlockAt
            ) {
                // is requested within current block
                TRequest storage last = requests[requestsCount - 1];
                last.shares += uint192(shares);
            } else {
                requests.push(TRequest(unlockAt, uint192(shares)));
            }
        } else {
            TRequest storage last = requests[requestsCount - 1];
            last.shares += uint192(shares);
            if (last.unlockAt < unlockAt) {
                last.unlockAt = unlockAt;
            }
        }
```

After merging, these requests become indivisible: `cancel()` and `finalizeWithFee()` operate only on entire request entries, so users cannot selectively cancel or early-exit part of their originally submitted withdrawals. All merged shares must be handled together.

This merge logic is inherited from `ERC20Cooldown / UnstakeCooldown,` but unlike those systems, `SharesCooldown` introduces `cancel()` and `finalizeWithFee()`, where per-request granularity matters.

Example scenario:

1. User submits a redemption of 100 shares (cooldown 7 days).

2. Later submits another redemption of 10 shares with the same unlock time (or after hitting the slot cap).

3. Both are merged into one request of 110 shares.

4. The user cannot cancel or early-exit only the 10 shares — any cancel() or finalizeWithFee() must act on all 110 shares.

**Recommended Mitigation:** Document that merged requests become indivisible for cancel and finalizeWithFee, or avoid merging and keep one request per redemption call.

**Strata:** Acknowledged.
