---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-2
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
title: Optimize away `bridgedMappingValue` variable in `TokenBridge::bridgeToken`
vuln_class: []
---

# Optimize away `bridgedMappingValue` variable in `TokenBridge::bridgeToken`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Optimize away `bridgedMappingValue` variable in `TokenBridge::bridgeToken` by for example:

```solidity
  function bridgeToken(
    address _token,
    uint256 _amount,
    address _recipient
  ) public payable nonZeroAddress(_token) nonZeroAddress(_recipient) nonZeroAmount(_amount) whenNotPaused nonReentrant {
    address nativeMappingValue = nativeToBridgedToken[sourceChainId][_token];

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
   // @audit remaining code continues unchanged
```

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L153-R188) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L153-R190).

**Cyfrin:** Verified.
