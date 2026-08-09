---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Uninitialized CCTP domain mapping can send USDC to the incorrect blockchain
vuln_class: []
---

# Uninitialized CCTP domain mapping can send USDC to the incorrect blockchain

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `USDCBridgeV2::chainIdToCCTPDomain` maps Wormhole chain IDs to Circle's CCTP domain IDs:
```solidity
mapping(uint16 => uint32) public chainIdToCCTPDomain;

function getCCTPDomain(uint16 _chain) internal view returns (uint32) {
    return chainIdToCCTPDomain[_chain];  // @audit returns 0 if not set!
}
```

**Impact:** When this mapping isn't initialized for a wormhole chain id, it returns 0 by default (Solidity's default value for `uint32`). However [Circle's CCTP domain 0 is Ethereum mainnet](https://developers.circle.com/cctp/cctp-supported-blockchains#cctp-v2-supported-domains). So if a mapping has not been configured for a given [wormhole chain id](https://wormhole.com/docs/products/reference/chain-ids/) eg (6 for Avalanche),`USDCBridgeV2::_transferUSDC` will happily send USDC to Ethereum instead of Avalanche:
```solidity
        circleTokenMessenger.depositForBurn(
            _amount,
            getCCTPDomain(_targetChain), // @audit 0 by default = Ethereum mainnet
            targetAddressBytes32,        // mintRecipient on destination
            USDC,          // burnToken
            destinationCallerBytes32,        // destinationCaller (restrict who can mint)
            0,
            1000
        );
```

**Recommended Mitigation:** The simplest option is to change `USDCBridgeV2::getCCTPDomain` to only allow domain 0 for wormhole's Ethereum chain id:
```solidity
function getCCTPDomain(uint16 _chain) internal view returns (uint32 domain) {
    domain = chainIdToCCTPDomain[_chain];
    // Wormhole ChainID 2 = Ethereum https://wormhole.com/docs/products/reference/chain-ids/
    // Only allow CCTP Domain 0 for Ethereum https://developers.circle.com/cctp/cctp-supported-blockchains#cctp-v2-supported-domains
    require(domain != 0 || _chain == 2, "CCTP domain not configured");
}
```

Another potential solution is to change `setBridgeAddress` such that it always sets the CCTP domain as well eg:
```solidity
    function setBridgeAddress(uint16 _chainId, address _bridgeAddress, uint32 _cctpDomain) external override onlyRole(DEFAULT_ADMIN_ROLE) {
        bridgeAddresses[_chainId] = _bridgeAddress;
        chainIdToCCTPDomain[_chain] = _cctpDomain;
        emit BridgeAddressAdd(_chainId, _bridgeAddress, _cctpDomain);
    }
```

Also consider changing `removeBridgeAddress` to delete from `chainIdToCCTPDomain` eg:
```solidity
    function removeBridgeAddress(uint16 _chainId) external override onlyRole(DEFAULT_ADMIN_ROLE) {
        delete bridgeAddresses[_chainId];
        delete chainIdToCCTPDomain[_chainId];
        emit BridgeAddressRemove(_chainId);
    }
```

**Securitize:** Fixed in commit [d750854](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/d750854aadd6873ad2be3aa95fd5abe80fa01bd3) by removing `setBridgeAddress` and adding a new function `setCCTPBridgeAddress` which enforces that CCTP Domain is configured at the same time as target bridge address for the same wormhole chain id. Also changed `removeBridgeAddress` to clear both mappings together as well.

**Cyfrin:** Verified.
