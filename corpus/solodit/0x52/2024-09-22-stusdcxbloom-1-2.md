---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-09-22-stusdcxbloom-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
tags:
- firm:0x52
- report:2024-09-22-stusdcxbloom
title: '[M-03] Using address rather than bytes32 for destinationAddress in wstUsdcBridge#bridgeWstUsdc
  causes incompatibility with chains that utilize 32 byte addresses'
vuln_class: []
---

# [M-03] Using address rather than bytes32 for destinationAddress in wstUsdcBridge#bridgeWstUsdc causes incompatibility with chains that utilize 32 byte addresses

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-09-22-stUSDCxBloom.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md)_

---

**Details**

[WstUsdcBridge.sol#L44-L49](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/messaging/WstUsdcBridge.sol#L44-L49)

    function bridgeWstUsdc(
        address destinationAddress, <- @audit uses address instead of bytes32
        uint256 wstUsdcAmount,
        uint32 dstEid,
        LzSettings calldata settings
    ) external payable returns (LzBridgeReceipt memory bridgingReceipt) {

wstUsdcBridge#bridgeWstUsdc utilizes type `address` for destinationAddress which breaks LZ compatibility with chains that use a 32 byte address instead of a 20 byte address like evm chains.

**Lines of Code**

[WstUsdcBridge.sol#L44-L58](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/messaging/WstUsdcBridge.sol#L44-L58)

**Recommendation**

Change destinationAddress from `address` to `bytes32`

**Remediation**

Fixed as recommended in stakeup-contracts [PR#92](https://github.com/stakeup-protocol/stakeup-contracts/pull/92)
