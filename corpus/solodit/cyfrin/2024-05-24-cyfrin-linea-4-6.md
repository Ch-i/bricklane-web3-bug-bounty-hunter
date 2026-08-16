---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Optimize away `nativeToken` variable in `TokenBridge::setDeployed`
vuln_class: []
---

# Optimize away `nativeToken` variable in `TokenBridge::setDeployed`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Optimize away `nativeToken` variable in `TokenBridge::setDeployed` which is written to but never read, eg:
```solidity
  function setDeployed(address[] calldata _nativeTokens) external onlyMessagingService onlyAuthorizedRemoteSender {
    // @audit remove `nativeToken`
    unchecked {
      for (uint256 i; i < _nativeTokens.length; ) {
        // @audit remove assignment nativeToken = _nativeTokens[i]
        nativeToBridgedToken[sourceChainId][_nativeTokens[i]] = DEPLOYED_STATUS;
        emit TokenDeployed(_nativeTokens[i]);
        ++i;
      }
    }
  }
```

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L303-L306) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L303-L306).

**Cyfrin:** Verified.
