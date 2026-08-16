---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`SecuritizeSwap::executeStableCoinTransfer` should use `SafeERC20` approval
  and transfer functions instead of standard `IERC20` functions'
vuln_class: []
---

# `SecuritizeSwap::executeStableCoinTransfer` should use `SafeERC20` approval and transfer functions instead of standard `IERC20` functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** In `SecuritizeSwap::executeStableCoinTransfer` use [`SafeERC20::forceApprove`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L101-L108) and [`SafeERC20::safeTransferFrom`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L43-L47):
```diff
    function executeStableCoinTransfer(address from, uint256 value) private {
        if (bridgeChainId != 0 && address(USDCBridge) != address(0)) {
-           stableCoinToken.transferFrom(from, address(this), value);
-           stableCoinToken.approve(address(USDCBridge), value);
+           SafeERC20.safeTransferFrom(stableCoinToken, from, address(this), value);
+           SafeERC20.forceApprove(stableCoinToken, address(USDCBridge), value);
            USDCBridge.sendUSDCCrossChainDeposit(bridgeChainId, issuerWallet, value);
        } else {
-           stableCoinToken.transferFrom(from, issuerWallet, value);
+           SafeERC20.safeTransferFrom(stableCoinToken, from, issuerWallet, value);
        }
    }
```

**Securitize:** `SecuritizeSwap` was removed as it was deprecated.

**Cyfrin:** Verified.
