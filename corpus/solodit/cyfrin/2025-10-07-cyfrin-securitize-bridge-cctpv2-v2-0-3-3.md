---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Refactor `SecuritizeBridge::bridgeDSTokens` and `quoteBridge` to use `internal`
  function saves 2 storage reads per bridging transaction
vuln_class: []
---

# Refactor `SecuritizeBridge::bridgeDSTokens` and `quoteBridge` to use `internal` function saves 2 storage reads per bridging transaction

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `SecuritizeBridge::bridgeDSTokens`:
* L71 calls `quoteBridge` which reads `wormholeRelayer` and `gasLimit` from storage
* L91 calls `wormholeRelayer.sendPayloadToEvm` which reads `wormholeRelayer` from storage again
* L108 reads `gasLimit` from storage again

Storage reads are expensive; refactor like this to avoid identical storage reads here:
```solidity
// new internal function
    function _quoteBridge(IWormholeRelayer relayer, uint256 _gasLimit, uint16 targetChain) internal view returns (uint256 cost) {
        (cost, ) = relayer.quoteEVMDeliveryPrice(targetChain, 0, _gasLimit);
    }

// modify `quoteBridge` to use new internal function
    function quoteBridge(uint16 targetChain) public override view returns (uint256 cost) {
        (cost, ) = _quoteBridge(wormholeRelayer, gasLimit, targetChain);
    }

// in `bridgeDSTokens` to cache `wormholeRelayer` and `gasLimit`
// then pass them to `_quoteBridge` and use them at L91 & L108
```

The same optimization should also be applied to `USDCBridgeV2::sendUSDCCrossChainDeposit`, `quoteBridge` and `_sendUSDCWithPayloadToEvm`.

**Securitize:** Fixed in commit [47c1ad0](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/47c1ad0de51887344785cebb7f5668b769b9d092).

**Cyfrin:** Verified.
