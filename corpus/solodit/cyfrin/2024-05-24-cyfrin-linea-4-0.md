---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: '`TokenBridge::deployBridgedToken` can use named return variable to avoid additional
  local variable'
vuln_class: []
---

# `TokenBridge::deployBridgedToken` can use named return variable to avoid additional local variable

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** `TokenBridge::deployBridgedToken` can use named return variable to avoid additional local variable, eg:

```solidity
  function deployBridgedToken(
    address _nativeToken,
    bytes calldata _tokenMetadata,
    uint256 _chainId
  ) internal returns (address bridgedTokenAddress) { // @audit named return
    bytes32 _salt = keccak256(abi.encode(_chainId, _nativeToken));
    BeaconProxy bridgedToken = new BeaconProxy{ salt: _salt }(tokenBeacon, "");
    bridgedTokenAddress = address(bridgedToken); // @audit assign to named return

    (string memory name, string memory symbol, uint8 decimals) = abi.decode(_tokenMetadata, (string, string, uint8));
    BridgedToken(bridgedTokenAddress).initialize(name, symbol, decimals);
    emit NewTokenDeployed(bridgedTokenAddress, _nativeToken);
    // @audit removed explicit return statement
  }
```

**Linea:**
Acknowledged; may be part of a future release.
