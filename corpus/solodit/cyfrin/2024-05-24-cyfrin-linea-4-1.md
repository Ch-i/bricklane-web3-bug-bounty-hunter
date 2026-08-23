---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-1
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
title: Reverse order of checks in `TokenBridge::isNewToken` to save 2 storage reads
vuln_class: []
---

# Reverse order of checks in `TokenBridge::isNewToken` to save 2 storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** `TokenBridge::isNewToken` can often save 2 storage reads by reversing the order of checks, eg:

```solidity
  modifier isNewToken(address _token) {
    // @audit swapped order of checks to save 2 storage reads by often failing on first check
    if (bridgedToNativeToken[_token] != EMPTY || nativeToBridgedToken[sourceChainId][_token] != EMPTY)
      revert AlreadyBridgedToken(_token);
    _;
  }
```

This way the modifier will almost always fail on the first check having done only 1 storage read, not triggering the 2 storage reads that occur in the second check.

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L68-R69) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L68-R68).

**Cyfrin:** Verified.
