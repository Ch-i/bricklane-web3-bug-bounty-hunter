---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-04-10-tokentable-fractionalizer-and-sellnow-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-04-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md
tags:
- firm:codespect
- report:2025-04-10-tokentable-fractionalizer-and-sellnow
title: '[L-02] Improper handling of cancelled token allocations in Fractionalizer'
vuln_class: []
---

# [L-02] Improper handling of cancelled token allocations in Fractionalizer

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-04-10-TokenTable-Fractionalizer-and-SellNow.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-04-10-TokenTable-Fractionalizer-and-SellNow.md)_

---

**Files:** [ShareFractionalizer.sol](https://github.com/EthSign/tokentable-sellnow-ft-fractionalizer-evm/blob/076d70abad50c2dddf8c5324c98d72f68ec6dc72/src/ShareFractionalizer.sol#L161-L195)

**Description:**

The `actual` in the unlocker represents the token allocation, which is distributed over time. The allocation can be cancelled in two ways: either by wiping out the pending claimable amount to prevent future claims, or by preserving the pending claimable amount for future distribution.

This can potentially cause issues on the `Fractionalizer` claiming side. For example:

- An `actual` is configured to distribute 2000 tokens;
- The fractionalizer splits this into four segments: (500, 500) at time X and (500, 500) at time Y, assigned to User A and User B, respectively;
- Before reaching time X (in the X/2), the actual is cancelled with no wiping, meaning that only 500 tokens could be claimed;
- Due to timing, front-running, or delayed admin actions, the segment shares are not updated by the time X is reached;
- User A calls `claim(...)` and successfully receives their 500-token share;
- User B, however, is unable to claim, as the total distributable amount has been depleted by User A;

This results in an unfair scenario where one user receives their allocation while another does not, even though both were entitled to equal shares under the original distribution.

**Impact:** Unfair distribution of tokens could arise if such an event occurs, leading to inconsistent or biased claims depending on timing and order of execution.

**Recommendation(s):** Consider updating the logic to handle this scenario fairly, or require that segments are updated before any further claims can be processed after cancellation.

**Status:** Acknowledged

**Update from TokenTable:** very unlikely scenario, resolving it will significantly increase gas cost. Decide to not patch.
