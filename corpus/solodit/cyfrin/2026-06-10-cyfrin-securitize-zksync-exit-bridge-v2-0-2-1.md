---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: Redundant SLOAD of `USDC` in `USDCBridgeV2::_transferUSDC`
vuln_class: []
---

# Redundant SLOAD of `USDC` in `USDCBridgeV2::_transferUSDC`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** `USDCBridgeV2::_transferUSDC` reads the `USDC` state variable from storage twice - once as the `forceApprove` target and once as the `burnToken` argument. Its only caller `sendUSDCCrossChainDeposit` has already cached `USDC` into the local `_USDC` before invoking it. Passing the cached value as a parameter eliminates two extra SLOADs on this hot per-bridge path.

```solidity
contracts/bridge/USDCBridgeV2.sol
211:        address _USDC = USDC;
219:        _transferUSDC(_amount, _targetChain, _recipient);
303:        IERC20(USDC).forceApprove(address(circleTokenMessenger), _amount);
312:            USDC,                               // burnToken
```

**Recommended Mitigation:** Add an `address _usdc` parameter to `_transferUSDC`, pass `_USDC` from `sendUSDCCrossChainDeposit`, and use it at both lines 303 and 312. The line-302 comment ("Reading storage variables explicitly to avoid Yul errors") no longer applies once the value arrives as a parameter. Consider also caching `circleTokenMessenger` inside `_transferUSDC` since it is read twice at lines 303, 307.

**Securitize:** Acknowledged.
