---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-05] The yield distribution methodology for stUSDC#poke will lead to substantial
  loss of yield due to MEV for both stUSDC and StakeUpStaking'
vuln_class: []
---

# [H-05] The yield distribution methodology for stUSDC#poke will lead to substantial loss of yield due to MEV for both stUSDC and StakeUpStaking

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[StUsdc.sol#L166-L185](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L166-L185)

    uint256 globalShares_ = _globalShares;
    uint256 protocolValue = _protocolValue(pool);
    uint256 newUsdPerShare = protocolValue.divWad(globalShares_);
    uint256 lastUsdPerShare = _lastUsdPerShare;

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
    } else if (newUsdPerShare < lastUsdPerShare) {
        // If the protocol has lost value, we need to update the USD per share to reflect the loss.
        _setUsdPerShare(newUsdPerShare);
    }

We see above that stUSDC#poke calculates the change in value of the last 24 hours and distributes it atomically to all current stakers. This leads to a significant opportunity to MEV the contract. Since there is no timelock or fees a user can do the following:

1. Borrow a large amount of USDC
2. Deposit the entire amount into stUSDC to own 95%+ of the pool
3. Call poke, receiving 95% of the rewards for themselves
4. Withdraw USDC from stUSDC
5. Repay flashloan

This allows them to steal nearly all the yield of the contract.

**Lines of Code**

[StUsdc.sol#L154-L190](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L154-L190)

**Recommendation**

Yield should be dripped to the contract over the course of 24 hours. Additionally deposits must be updated to account for the yield being dripped so that they do not accrue more value than they should. StakeUpStaking also suffers from a similar issue and I would recommend adding a deposit timelock.

**Remediation**

Fixed as recommended in stakeup-contracts [PR#89](https://github.com/stakeup-protocol/stakeup-contracts/pull/89) (reward drip), [PR#91](https://github.com/stakeup-protocol/stakeup-contracts/pull/91) (deposit timelock) and [PR#96](https://github.com/stakeup-protocol/stakeup-contracts/pull/96) (tby discount)
