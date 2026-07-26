---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-4-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Save 1 storage read in `TokenBridge::removeReserved` by caching `sourceChainId`
vuln_class: []
---

# Save 1 storage read in `TokenBridge::removeReserved` by caching `sourceChainId`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** `sourceChainId` is read from storage twice in `TokenBridge::removeReserved` so caching it can save 1 storage read, eg:
```solidity
  function removeReserved(address _token) external nonZeroAddress(_token) onlyOwner {
    // @audit cache `sourceChainId`
    uint256 sourceChainIdCache = sourceChainId;

    // @audit used cached version
    if (nativeToBridgedToken[sourceChainIdCache][_token] != RESERVED_STATUS) revert NotReserved(_token);
    nativeToBridgedToken[sourceChainIdCache][_token] = EMPTY;
  }
```

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L367-R367) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L367-R370).

**Cyfrin:** Verified.
