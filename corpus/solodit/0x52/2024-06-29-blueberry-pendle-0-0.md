---
affected_contracts: []
derives_from: []
id: solodit-0x52-2024-06-29-blueberry-pendle-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-06-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-06-29-Blueberry-Pendle.md
tags:
- firm:0x52
- report:2024-06-29-blueberry-pendle
title: '[M-01] PT donation attack will DOS spell deposit permanently'
vuln_class: []
---

# [M-01] PT donation attack will DOS spell deposit permanently

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2024-06-29-Blueberry-Pendle.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-06-29-Blueberry-Pendle.md)_

---

**Details**

[PendleSpell.sol#L128-L137](https://github.com/Blueberryfi/blueberry-core/blob/d0ed24769704cf5d9a8b0616cf534f29db32f6ca/contracts/spell/PendleSpell.sol#L128-L137)

    (uint256 ptAmount, , ) = IPendleRouter(_pendleRouter).swapExactTokenForPt(
        address(this),
        market,
        minPtOut,
        params,
        input,
        limitOrder
    );

    if (ptAmount != IERC20Upgradeable(pt).balanceOf(address(this))) revert Errors.SWAP_FAILED(pt);

After swapping from debt token to PT, the contract makes an exact check against the balance of the contract to ensure the swap executed as expected. The issue with this is that even if it is a single wei over, the contract will revert. This makes it trivial to permanently DOS opening positions via the contract by donating a small amount of PT to the contract.

**Lines of Code**

[PendleSpell.sol#L101-L147](https://github.com/Blueberryfi/blueberry-core/blob/d0ed24769704cf5d9a8b0616cf534f29db32f6ca/contracts/spell/PendleSpell.sol#L101-L147)

**Recommendation**

Check should be `>` rather than `!=`

**Remediation**

Fixed as suggested.
