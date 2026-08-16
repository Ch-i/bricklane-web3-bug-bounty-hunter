---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-05-23-mozaic-archimedes-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md
tags:
- firm:trust-security
- report:2023-05-23-mozaic-archimedes
title: TRST-L-4 Vault will fail to operate plugins with USDT due to lack of zero approval
vuln_class: []
---

# TRST-L-4 Vault will fail to operate plugins with USDT due to lack of zero approval

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-05-23-Mozaic Archimedes.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-05-23-Mozaic%20Archimedes.md)_

---

**Description:**
Admins can trigger the execute() function to interact with plugins.
```solidity
        if(_actionType == IPlugin.ActionType.Stake) {
                 (uint256 _amountLD, address _token) = abi.decode(_payload, (uint256, address));
        IERC20(_token).approve(supportedPlugins[_pluginId].pluginAddr, _amountLD);
                } else if(_actionType == IPlugin.ActionType.SwapRemote) {
                     (uint256 _amountLD, address _token, , ) = abi.decode(_payload, 
                         (uint256, address, uint16, uint256));
                 IERC20(_token).approve(supportedPlugins[_pluginId].pluginAddr, 
        _amountLD);
        }
        IPlugin(supportedPlugins[_pluginId].pluginAddr).execute(_actionType, 
        _payload);
```
Some tokens like USDT will revert when calling `approve()` when the previous allowance is not 
zero (to protect against a well-known double-allowance attack). Therefore, if the plugin does 
not consume the entire allowance, in the next `execute()` call the function will revert.

**Recommended mitigation:**
Call approve(token, 0) before setting the desired approval.

**Team response:**
Fixed.

**Mitigation review:**
Similar to M-8, the issue has been fixed correctly in the Vault, but unsafe approvals remain in 
the StargatePlugin contract.
