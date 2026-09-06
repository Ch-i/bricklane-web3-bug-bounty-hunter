---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: User lock and earning might contain empty elements.
vuln_class: []
---

# User lock and earning might contain empty elements.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: _cleanWithdrawableLocks(), line 1123. 
MultiFee Distribution.sol: withdraw(), line 775 
After the lock withdrawal, the contract deletes it with "delete" operator. However, deleting elements of an array with this operator only sets the value of an element to 0, and the element will still be present in the array. Due to this, the array `userLocks [user]` might contain empty elements, iteration through which will increase gas spending. This is why it is recommended to shift elements in the array to the left by 1 when any element is removed from the array. The issue is marked as medium-risk, since if there are too many elements in an array, a transaction might revert due to an "out of gas" error and even not fit in one block. 

**Recommendation**: 

Shift elements in the array when removing an element, so that there are no empty elements in the array. 

**Post-audit**: 

Both "userLocks" and "userEarnings" are cleaned now.
