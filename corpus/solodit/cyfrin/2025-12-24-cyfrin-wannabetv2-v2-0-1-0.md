---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Use `SafeERC20` functions instead of standard ERC20 functions
vuln_class: []
---

# Use `SafeERC20` functions instead of standard ERC20 functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Use [SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) functions `safeTransfer`, `safeTransferFrom`, `forceApprove` etc instead of standard ERC20 functions to ensure support for ERC20 tokens with non-standard behavior:
```solidity
Bet.sol
63:        IERC20(initialBet.asset).transferFrom(
71:            IERC20(initialBet.asset).approve(pool, type(uint256).max);
114:        IERC20(b.asset).transferFrom(msg.sender, address(this), b.takerStake);
150:        IERC20(b.asset).transfer(winner, totalWinnings);
155:            IERC20(b.asset).transfer(_treasury, remainder);
193:        try IERC20(b.asset).transfer(b.maker, makerRefund) {} catch {}
194:        try IERC20(b.asset).transfer(b.taker, takerRefund) {} catch {}
```

**WannaBet:** Fixed in commit [b571b26](https://github.com/gskril/wannabet-v2/commit/b571b26b093d20ab5d876fa0f8845671e1b6e80b).

**Cyfrin:** Verified.
