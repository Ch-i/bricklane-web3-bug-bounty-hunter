---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Use `SafeERC20` approval and transfer functions instead of standard IERC20
  functions
vuln_class: []
---

# Use `SafeERC20` approval and transfer functions instead of standard IERC20 functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Use [SafeERC20::forceApprove](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L105-L110) and `safeTransfer` functions instead of standard IERC20 functions:
```solidity
wormhole/WormholeCCTPUpgradeable.sol
121:        IERC20(USDC).approve(address(circleTokenMessenger), amount);

bridge/USDCBridgeV2.sol
150:        IERC20(USDC).transferFrom(_msgSender(), address(this), _amount);
264:        IERC20(USDC).approve(address(circleTokenMessenger), _amount);
```

**Securitize:** Fixed in commit [d75ac6f](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/d75ac6fb219f2f536172e4c7b146cece27ca175e).

**Cyfrin:** Verified.
