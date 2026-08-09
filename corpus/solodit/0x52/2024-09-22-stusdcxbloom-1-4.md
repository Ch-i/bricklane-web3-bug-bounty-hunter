---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-1-4
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
title: '[M-05] In the event of yield loss, yield will be double counted leading to
  excess fees'
vuln_class: []
---

# [M-05] In the event of yield loss, yield will be double counted leading to excess fees

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[StUsdc.sol#L171-L181](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L171-L181)

    if (newUsdPerShare > lastUsdPerShare) {
        uint256 yieldPerShare = newUsdPerShare - lastUsdPerShare;
        // Calculate performance fee
        uint256 fee = _calculateFee(yieldPerShare, globalShares_);
        // Calculate the new total value of the protocol for users
        uint256 userValue = protocolValue - fee;
        newUsdPerShare = userValue.divWad(globalShares_);
        // Update state to distribute yield to users
        _setUsdPerShare(newUsdPerShare);
        // Process fee to StakeUpStaking
        _processFee(fee);

Whenever yield is accumulated by the contract, a fee is taken. In itself this is fine but it can lead to double counted yield in the event that the share price decrease. Take the following example, the share price increases from 1 -> 1.1. A fee will be taken on the 0.1 share price gain. Now the token decreases and increases again as follows 1.1 -> 1.05 -> 1.1. On the move from 1.05 -> 1.1 the fee will be taken again, effectively double charging fees to the users.

**Lines of Code**

[StUsdc.sol#L154-L190](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L154-L190)

**Recommendation**

The contract should implement a highwater tracker for the share price and only pay out fees for increase above that mark.

**Remediation**

Fixed as recommended in stakeup-contracts [PR#89](https://github.com/stakeup-protocol/stakeup-contracts/pull/89)
