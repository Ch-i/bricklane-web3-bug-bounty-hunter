---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Optimize away `nativeMappingValue` variable in `TokenBridge::completeBridging`
vuln_class: []
---

# Optimize away `nativeMappingValue` variable in `TokenBridge::completeBridging`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Optimize away `nativeMappingValue` variable in `TokenBridge::completeBridging` by for example:
```solidity
  function completeBridging(
    address _nativeToken,
    uint256 _amount,
    address _recipient,
    uint256 _chainId,
    bytes calldata _tokenMetadata
  ) external nonReentrant onlyMessagingService onlyAuthorizedRemoteSender whenNotPaused {
    // @audit remove `nativeMappingValue` and instead
    // initialize `bridgedToken`
    address bridgedToken = nativeToBridgedToken[_chainId][_nativeToken];

    // @audit use `bridgedToken` for the check
    if (bridgedToken == NATIVE_STATUS || bridgedToken == DEPLOYED_STATUS) {
      // Token is native on the local chain
      IERC20Upgradeable(_nativeToken).safeTransfer(_recipient, _amount);
    } else {
       // @audit remove assignment `bridgedToken = nativeMappingValue;`
       //
       // @audit use `bridgedToken` for the check
      if (bridgedToken == EMPTY) {
        // New token
        bridgedToken = deployBridgedToken(_nativeToken, _tokenMetadata, sourceChainId);
        bridgedToNativeToken[bridgedToken] = _nativeToken;
        nativeToBridgedToken[targetChainId][_nativeToken] = bridgedToken;
      }
      BridgedToken(bridgedToken).mint(_recipient, _amount);
    }

    emit BridgingFinalized(
      _nativeToken,
      // @audit return 0 address as before if token was native on local chain
      bridgedToken == NATIVE_STATUS || bridgedToken == DEPLOYED_STATUS ? address(0x0) : bridgedToken,
      _amount,
      _recipient);
  }
```

**Linea:**
Acknowledged; will be part of a future release.
