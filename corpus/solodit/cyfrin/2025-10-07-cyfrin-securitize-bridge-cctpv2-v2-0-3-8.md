---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Pass `_refundChain` as input to `USDCBridgeV2::_buildCCTPKey` saves 1 storage
  read and external call
vuln_class: []
---

# Pass `_refundChain` as input to `USDCBridgeV2::_buildCCTPKey` saves 1 storage read and external call

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `USDCBridgeV2::sendUSDCCrossChainDeposit` passes `wormhole.chainId()` as the third-to-last parameter:
```solidity
        _sendUSDCWithPayloadToEvm(
            _targetChain,
            targetBridge, // address (on targetChain) to send token and payload to
            payload,
            0, // receiver value
            gasLimit,
            _amount,
            wormhole.chainId(), // @audit `_refundChain`
            address(this),
            deliveryCost
        );
```

But then `_sendUSDCWithPayloadToEvm` calls `_buildCCTPKey` which performs the same work again:
```solidity
    function _buildCCTPKey() private view returns (MessageKey memory) {
        return MessageKey(CCTP_KEY_TYPE, abi.encodePacked(getCCTPDomain(wormhole.chainId()), uint64(0)));
    }
```

Refactor `_buildCCTPKey` to take `uint16 _whSourceChain` as an input parameter and use it like this:
```solidity
    function _buildCCTPKey(uint16 _whSourceChain) private view returns (MessageKey memory) {
        return MessageKey(CCTP_KEY_TYPE, abi.encodePacked(getCCTPDomain(_whSourceChain), uint64(0)));
    }
```

**Securitize:** Acknowledged.

\clearpage
