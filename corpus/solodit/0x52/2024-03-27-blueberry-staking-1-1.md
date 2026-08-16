---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-03-27-blueberry-staking-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-03-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md
tags:
- firm:0x52
- report:2024-03-27-blueberry-staking
title: '[M-02] It is impossible to complete any vest unless all vests are mature'
vuln_class: []
---

# [M-02] It is impossible to complete any vest unless all vests are mature

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-03-27-Blueberry-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-03-27-Blueberry-Staking.md)_

---

**Details**

[BlueberryStaking.sol#L328-L331](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L328-L331)

    uint256 vestIndexLength = vests.length;
    if (vesting[msg.sender].length < vestIndexLength) {
        revert InvalidLength();
    }

The above lines cache the incorrect array length. It should cache the length of \_vestIndexes but instead caches the length of vests.

[BlueberryStaking.sol#L334-L348](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L334-L348)

    for (uint256 i; i < vestIndexLength; ++i) {
        Vest storage v = vests[_vestIndexes[i]];

        if (!isVestingComplete(msg.sender, _vestIndexes[i])) {
            revert VestingIncomplete();
        }

        totalbdblb += v.amount + v.extra;

        // Ensure accurate redistribution accounting for accelerations.
        totalVestAmount -= v.amount;
        redistributedBLB -= v.extra;

        delete vests[_vestIndexes[i]];
    }

This error causes and OOB error when accessing \_vestIndexes unless is it as least the same length as vests. The result is that the user must vest all at the same time or their call will revert. If even a single vest isn't mature then none will be able to be vested.

**Lines of Code**

[BlueberryStaking.sol#L324-L355](https://github.com/Blueberryfi/blueberry-staking/blob/efaf7fc690e38914ba475d5ac61a4d0bd3f45c0d/src/BlueberryStaking.sol#L324-L355)

**Recommendation**

Use `_vestIndexes.length` instead of `vests.length`

**Remediation**

Fixed in [PR#24](https://github.com/Blueberryfi/blueberry-staking/pull/24) as recommended.
