---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-28-orbital-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-28T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md
tags:
- firm:trust-security
- report:2023-05-28-orbital-finance
title: TRST-M-1 Removing a trade path in router will cause serious data corruption
vuln_class: []
---

# TRST-M-1 Removing a trade path in router will cause serious data corruption

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-28-Orbital Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-28-Orbital%20Finance.md)_

---

**Description:**
The RouterInfo represents a single UniV3-compatible router which supports a list of token 
paths. It uses the following data structures:
```solidity
         mapping(address => mapping(address => listInfo)) private allowedPairsMap;
                  pair[] private allowedPairsList;
```

```solidity
          struct listInfo {
               bool allowed;
                uint256 listPosition;
         }
         struct pair {
            address token0;
               address token1;
                  uint256 numPathsAllowed;
          }
```

When an admin specifies a new path from **token0** to **token1**, `_increasePairPaths()` is called. 
```solidity
               function _increasePairPaths(address token0, address token1) private {
                     listInfo storage LI = allowedPairsMap[token0][token1];
                  if (!LI.allowed){
                  LI.allowed = true;
                  LI.listPosition = allowedPairsList.length;
                      allowedPairsList.push(pair(token0, token1, 0));
                   }
                      allowedPairsList[LI.listPosition].numPathsAllowed++;
                   }
```
When a path is removed, the complementary function is called.
```solidity
      function _decreasePairPaths(address token0, address token1) private {
             listInfo storage LI = allowedPairsMap[token0][token1];
                require(LI.allowed, "RouterInfo: pair not allowed");
                   allowedPairsList[LI.listPosition].numPathsAllowed--;
            if (allowedPairsList[LI.listPosition].numPathsAllowed == 0){
         allowedPairsList[LI.listPosition] = 
      allowedPairsList[allowedPairsList.length - 1];
         allowedPairsList.pop();
         LI.allowed = false;
      }
      }
```
When the last path is removed, the contract reuses the index of the removed pair, to store 
the last pair in the list. It then removes the last pair, having already copied it. The issue is that 
the corresponding **listInfo** structure is not updated, to keep track of index in the pairs list. 
Future usage of the last pair will use a wrong index, which at this moment, is over the array 
bounds. When a new pair will be created, it will share the index with the corrupted pair. This 
can cause a variety of serious issues. For example, it will not be possible to remove paths from 
the corrupted pair until a new pair is created, at which point the new pair will have a wrong 
**numPathsAllowed** as it is shared.


**Recommended Mitigation:**
Update the **listPosition** member of the last pair in the list, before repositioning it.


**Team Response:**
"Added 'lastPair' variable, which is used to point what was the last pair, to the new location in 
the list."

**Mitigation review:**
The fix is simple and correct.
