---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use `SafeERC20` functions instead of standard `ERC20` transfer functions
vuln_class: []
---

# Use `SafeERC20` functions instead of standard `ERC20` transfer functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Use [`SafeERC20`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) functions instead of standard `ERC20` transfer functions:

```solidity
$ rg "transferFrom" && rg "transfer\("
RWAToken/DividendManager.sol
317:        $._stablecoin.transferFrom(

RWAToken/RemoraToken.sol
220:     * @dev Calls OpenZeppelin ERC20Upgradeable transferFrom function.
251:        return super.transferFrom(from, to, value);
344:            $._stablecoin.transferFrom(sender, $._wallet, _transferFee);
352:     * @dev Calls OpenZeppelin ERC20Upgradeable transferFrom function.
358:    function transferFrom(
376:            $._stablecoin.transferFrom(sender, $._wallet, _transferFee);
379:        return super.transferFrom(from, to, value);

TokenBank.sol
261:        IERC20(stablecoin).transferFrom(

PledgeManager.sol
196:        IERC20(stablecoin).transferFrom(

RemoraIntermediary.sol
172:        IERC20(data.assetReceived).transferFrom(
177:        IERC20(data.assetSold).transferFrom(
197:        IERC20(data.assetReceived).transferFrom(
238:        IERC20(data.paymentToken).transferFrom(
269:            IERC20(data.paymentToken).transferFrom(
296:        IERC20(data.paymentToken).transferFrom(
331:        IERC20(token).transferFrom(payer, recipient, amount);
RWAToken/DividendManager.sol
409:            $._stablecoin.transfer(holder, payoutAmount);
429:        stablecoin.transfer($._wallet, valueToClaim);

RWAToken/RemoraToken.sol
401:        $._stablecoin.transfer(account, burnPayout);

TokenBank.sol
185:        IERC20(tokenAddress).transfer(to, amount);
206:        if (amount != 0) IERC20(stablecoin).transfer(to, amount);
237:        IERC20(stablecoin).transfer(custodialWallet, totalValue);
266:        IERC20(tokenAddress).transfer(to, amount);

PledgeManager.sol
237:                _stablecoin.transfer(feeWallet, feeValue);
239:            _stablecoin.transfer(destinationWallet, amount);
299:        IERC20(stablecoin).transfer(signer, _fixDecimals(refundAmount + fee));
```

**Remora:** Fixed in commit [f2f3f7e](https://github.com/remora-projects/remora-smart-contracts/commit/f2f3f7e8d51a018417615207152d9fbadf8484eb).

**Cyfrin:** Verified.
