---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-0-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[H-06] Shares of stUSDC can be lost/gained during cross chain transfers due
  to differing conversion rates across chains'
vuln_class: []
---

# [H-06] Shares of stUSDC can be lost/gained during cross chain transfers due to differing conversion rates across chains

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[StUsdcLite.sol#L418-L428](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdcLite.sol#L418-L428)

    function _debit(uint256 _amountLD, uint256 _minAmountLD, uint32 _dstEid)
        internal
        override
        returns (uint256 amountSentLD, uint256 amountReceivedLD)
    {
        (amountSentLD, amountReceivedLD) = _debitView(_amountLD, _minAmountLD, _dstEid);


        uint256 shares = sharesByUsd(amountSentLD);
        _burnShares(msg.sender, shares);
        _setTotalUsd(_getTotalUsd() - amountSentLD);
    }

[StUsdcLite.sol#L430-L438](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdcLite.sol#L430-L438)

    function _credit(address _to, uint256 _amountToCreditLD, uint32 /*_srcEid*/ )
        internal
        override
        returns (uint256 amountReceivedLD)
    {
        _mintShares(_to, sharesByUsd(_amountToCreditLD));
        _setTotalUsd(_getTotalUsd() + _amountToCreditLD);
        return _amountToCreditLD;
    }

We see above that when sending payments that value is converted to shares to burn but then the value is the amount transferred. This is confirmed by \_credit where we see that the \_amountToCreditLD is converted to shares.

This creates an issue when if the if the transfer is in progress when poke is called. This means the conversion rate will higher or lower than when it was sent, resulting in shares being lost or gained during transit. Shares gained can result in the contract being undercollateralized.

**Lines of Code**

[StUsdcLite.sol#L418-L438](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdcLite.sol#L418-L438)

**Recommendation**

Cross chain transfers should send shares NOT value since shares are constant and value is not.

**Remediation**

Fixed as recommended in stakeup-contracts [PR#93](https://github.com/stakeup-protocol/stakeup-contracts/pull/93)
