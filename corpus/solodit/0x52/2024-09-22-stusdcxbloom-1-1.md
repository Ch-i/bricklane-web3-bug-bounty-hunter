---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[M-02] In the event of a partial match inside \_convertMatchOrders, borrower
  funds will be over-allocated'
vuln_class: []
---

# [M-02] In the event of a partial match inside \_convertMatchOrders, borrower funds will be over-allocated

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[BloomPool.sol#L399-L403](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L399-L403)

    if (lenderFunds == matches[index].lCollateral) {
        matches.pop();
    } else {
        matches[index].lCollateral -= uint128(lenderFunds);
    }

Above is the final portion of the matching loop in which filled orders are handled. `lenderFunds == matches[index].lCollateral` indicates the order has been fully matched. In this scenario it is correctly popped. The other case is when the the match is partially filled. We see that lCollateral is decreased but bCollateral is not. The result is that borrower funds can be double filled. This creates a shortfall in funds that can only be remedied by donating the over-allocated funds to the contract.

**Lines of Code**

[BloomPool.sol#L377-L416](https://github.com/Blueberryfi/bloom-v2/blob/87a60380331cc914be41ad57691f08b532a4d6fb/src/BloomPool.sol#L377-L416)

**Recommendation**

`matches[index].lCollateral` should also be decremented

**Remediation**

Fixed as recommended in bloom-v2 [PR#16](https://github.com/Blueberryfi/bloom-v2/pull/16)
