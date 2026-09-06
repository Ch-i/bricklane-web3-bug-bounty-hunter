---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache storage to prevent identical storage reads:
* `contracts/wormhole/WormholeCCTPUpgradeable.sol`
```solidity
// cache `USDC` in `redeemUSDC`
65:        uint256 beforeBalance = IERC20(USDC).balanceOf(address(this));
67:        return IERC20(USDC).balanceOf(address(this)) - beforeBalance;
```

* `contracts/bridge/SecuritizeBridge.sol`
```solidity
// cache `dsToken` in `bridgeDSTokens`
73:        require(dsToken.balanceOf(_msgSender()) >= value, "Not enough balance in source chain to bridge");
88:        dsToken.burn(_msgSender(), value, BRIDGE_REASON);
108:        emit DSTokenBridgeSend(targetChain, address(dsToken), _msgSender(), value);

// cache `dsToken` in `receiveWormholeMessages`
144:        dsToken.issueTokens(investorWallet, value);
146:        emit DSTokenBridgeReceive(sourceChain, address(dsToken), investorWallet, value);
```

* `contracts/bridge/USDCBridgeV2.sol`
```solidity
// cache `USDC` in `sendUSDCCrossChainDeposit`
143:        if (IERC20(USDC).balanceOf(_msgSender()) < _amount) {
150:        IERC20(USDC).transferFrom(_msgSender(), address(this), _amount);
// also change `_transferUSDC` to take cached `USDC` as parameter to save
// 2 storage reads inside `_transferUSDC`;
// cache `USDC, `circleTokenMessenger` in `_transferUSDC`
264:        IERC20(USDC).approve(address(circleTokenMessenger), _amount);
268:        circleTokenMessenger.depositForBurn(
272:            USDC,          // burnToken
```

**Securitize:** Acknowledged.
