---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-1-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-M-10 MozBridge underestimates gas for sending of Moz messages
vuln_class: []
---

# TRST-M-10 MozBridge underestimates gas for sending of Moz messages

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
The bridge calculates LayerZero fees for sending Mozaic messages using the function below:
```solidity
        function quoteLayerZeroFee(uint16 _chainId, uint16 _msgType, LzTxObj memory _lzTxParams) public view returns (uint256 _nativeFee, uint256 _zroFee) { 
             bytes memory payload = "";
        if (_msgType == TYPE_REPORT_SNAPSHOT) {
                payload = abi.encode(TYPE_REPORT_SNAPSHOT);
        }
        else if (_msgType == TYPE_REQUEST_SNAPSHOT) {
                     payload = abi.encode(TYPE_REQUEST_SNAPSHOT);
        }
        else if (_msgType == TYPE_SWAP_REMOTE) {
                        payload = abi.encode(TYPE_SWAP_REMOTE);
        }
        else if (_msgType == TYPE_STAKE_ASSETS) {
                          payload = abi.encode(TYPE_STAKE_ASSETS);
        }   
        else if (_msgType == TYPE_UNSTAKE_ASSETS) {
                                 payload = abi.encode(TYPE_UNSTAKE_ASSETS);
        }
        else if (_msgType == TYPE_REPORT_SETTLE) {
                                 payload = abi.encode(TYPE_REPORT_SETTLE);
        }
        else if (_msgType == TYPE_REQUEST_SETTLE) {
                            payload = abi.encode(TYPE_REQUEST_SETTLE);
        }
        else {
                         revert("MozBridge: unsupported function type");
        }
        
                     bytes memory _adapterParams = _txParamBuilder(_chainId, _msgType, _lzTxParams);
              return layerZeroEndpoint.estimateFees(_chainId, address(this), 
       payload, useLayerZeroToken, _adapterParams);
        }
```
The issue is that the actual payload used for Mozaic messages is longer than the one calculated 
above. For example, REPORT_SNAPSHOT messages include a **Snapshot** structure.
 ```solidity
            struct Snapshot {
               uint256 depositRequestAmount;
                 uint256 withdrawRequestAmountMLP;
                     uint256 totalStablecoin;
                         uint256 totalMozaicLp; // Mozaic "LP"
                             uint8[] pluginIds;
                                 address[] rewardTokens;
                                  uint256[] amounts;
                   }
```
Undercalculation of gas fees will cause insufficient gas to be sent to the bridge, reverting the 
`send()` transaction. 

**Recommended mitigation:**
Error on the side of caution and estimate a larger than expected fee.

**Team response:**
Fixed.

**Mitigation review:**
The code now uses the correct payload for estimating fees.
