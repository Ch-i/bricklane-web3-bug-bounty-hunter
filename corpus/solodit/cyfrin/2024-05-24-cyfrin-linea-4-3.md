---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Save 2 storage reads in `TokenBridge::bridgeToken` by caching `sourceChainId`
vuln_class: []
---

# Save 2 storage reads in `TokenBridge::bridgeToken` by caching `sourceChainId`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** `sourceChainId` is always read once at the beginning of `TokenBridge::bridgeToken` [L153](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/tokenBridge/TokenBridge.sol#L153).

Then in the `else` branch of `TokenBridge::bridgeToken`, `sourceChainId` is always read at least once [L191](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/tokenBridge/TokenBridge.sol#L191) but can also be read a second time [L183](https://github.com/Consensys/zkevm-monorepo/blob/364b64d2a2704567adac00e3fa428a1901717666/contracts/contracts/tokenBridge/TokenBridge.sol#L183).

Hence it is more efficient to cache `sourceChainId` at the beginning of `TokenBridge::bridgeToken` to save 2 storage reads. The optimized version of `bridgeToken` found below also contains the optimization from the previous issue _"Optimize away bridgedMappingValue variable in TokenBridge::bridgeToken"_ which is required to get around the "stack too deep" error this optimization would otherwise create:
```solidity
  function bridgeToken(
    address _token,
    uint256 _amount,
    address _recipient
  ) public payable nonZeroAddress(_token) nonZeroAddress(_recipient) nonZeroAmount(_amount) whenNotPaused nonReentrant {
    // @audit cache `sourceChainId` and use it when setting `nativeMappingValue`
    uint256 sourceChainIdCache = sourceChainId;
    address nativeMappingValue = nativeToBridgedToken[sourceChainIdCache][_token];

    if (nativeMappingValue == RESERVED_STATUS) {
      // Token is reserved
      revert ReservedToken(_token);
    }

    // @audit remove `bridgedMappingValue` and
    // instead initialize `nativeToken`
    address nativeToken = bridgedToNativeToken[_token];
    uint256 chainId;
    bytes memory tokenMetadata;

    // @audit use `nativeToken` in the comparison
    if (nativeToken != EMPTY) {
      // Token is bridged
      BridgedToken(_token).burn(msg.sender, _amount);
      // @audit remove assignment `nativeToken = bridgedMappingValue`
      chainId = targetChainId;
    } else {
      // Token is native

      // For tokens with special fee logic, ensure that only the amount received
      // by the bridge will be minted on the target chain.
      uint256 balanceBefore = IERC20Upgradeable(_token).balanceOf(address(this));
      IERC20Upgradeable(_token).safeTransferFrom(msg.sender, address(this), _amount);
      _amount = IERC20Upgradeable(_token).balanceOf(address(this)) - balanceBefore;

      nativeToken = _token;

      if (nativeMappingValue == EMPTY) {
        // New token
        // @audit using cached `sourceChainIdCache`
        nativeToBridgedToken[sourceChainIdCache][_token] = NATIVE_STATUS;
        emit NewToken(_token);
      }

      // Send Metadata only when the token has not been deployed on the other chain yet
      if (nativeMappingValue != DEPLOYED_STATUS) {
        tokenMetadata = abi.encode(_safeName(_token), _safeSymbol(_token), _safeDecimals(_token));
      }
      // @audit using cached `sourceChainIdCache`
      chainId = sourceChainIdCache;
    }

    messageService.sendMessage{ value: msg.value }(
      remoteSender,
      msg.value, // fees
      abi.encodeCall(ITokenBridge.completeBridging, (nativeToken, _amount, _recipient, chainId, tokenMetadata))
    );
    emit BridgingInitiated(msg.sender, _recipient, _token, _amount);
  }
```

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L153-R188) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L153-R190).

**Cyfrin:** Verified.
