---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: '`SDLVesting::vestedAmount` gas optimizations'
vuln_class: []
---

# `SDLVesting::vestedAmount` gas optimizations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The `SDLVesting::vestedAmount` function computes the `totalAllocation` before the `if (_timestamp < start) return 0;` check. In the event that check returns true and the function returns 0 then the gas spent on that computation is wasted.
Moreover, given that the condition of `_timestamp < start` is checked the final return `return (totalAllocation * (_timestamp - start)) / duration;` can be done in an unchecked block to save gas:

```diff
    function vestedAmount(uint64 _timestamp) public view returns (uint256) {
+       if (_timestamp < start) {
+            return 0;

        uint256 totalAllocation = sdlToken.balanceOf(address(this)) + released;

-      if (_timestamp < start) {
-           return 0;
-       } else if (_timestamp > start + duration) {
-           return totalAllocation;
-       } else if (vestingTerminated) {
-           return totalAllocation;
-       } else {
-           return (totalAllocation * (_timestamp - start)) / duration;
+       if (_timestamp > start + duration) {
+           return totalAllocation;
+      } else if (vestingTerminated) {
+           return totalAllocation;
+      } else {
+           unchecked {
+               return (totalAllocation * (_timestamp - start)) / duration;
+           }
        }
    }
```

**Stake.Link:** Acknowledged.
