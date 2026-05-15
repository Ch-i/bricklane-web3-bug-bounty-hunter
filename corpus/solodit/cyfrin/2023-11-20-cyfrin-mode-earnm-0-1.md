---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Transferring mystery boxes bricks token redemption
vuln_class: []
---

# Transferring mystery boxes bricks token redemption

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** `MysteryBox` is an `ERC1155` contract which users expect to be able to transfer to other addresses via the in-built transfer functions. But `MysteryBox::claimMysteryBoxes()` [reverts](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L296) unless the caller is the same address who minted the box since the internal mappings that track mystery box ownership are never updated when transfers occur.

**Impact:** Token redemption is bricked if users transfer their mystery box. Users reasonably expect to be able to transfer their mystery box from one address they control to another address (if for example their first address is compromised), or they may wish to sell their mystery box on platforms like OpenSea which support `ERC1155` sales.

**Recommended Mitigation:** Override `ERC1155` transfer hooks to either prevent transferring of mystery boxes, or to update the internal mappings such that when mystery boxes are transferred the new owner address can redeem their tokens. The second option may be more attractive for the protocol as it allows mystery box holders to access liquidity without putting sell pressure on the token, creating a "secondary market" for mystery boxes.

**Mode:**
Fixed in commit [a65a50c](https://github.com/Earnft/smart-contracts/commit/a65a50ca8af4d6abc58d3c429785bcd82182c04e) by overriding `ERC1155::_beforeTokenTransfer()` to prevent mystery boxes from being transferred.

**Cyfrin:** Verified.
