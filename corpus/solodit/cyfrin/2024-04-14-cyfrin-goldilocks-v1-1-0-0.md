---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: '`Goldilend.lock()` will always revert'
vuln_class: []
---

# `Goldilend.lock()` will always revert

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** High

**Description:** In `lock()`, it calls `_refreshiBGT()` before pulling `iBGT` from the user and will revert while calling `iBGTVault(ibgtVault).stake()`.

```solidity
  function lock(uint256 amount) external {
    uint256 mintAmount = _GiBGTMintAmount(amount);
    poolSize += amount;
    _refreshiBGT(amount); //@audit should call after depositing funds
    SafeTransferLib.safeTransferFrom(ibgt, msg.sender, address(this), amount);
    _mint(msg.sender, mintAmount);
    emit iBGTLock(msg.sender, amount);
  }
...
  function _refreshiBGT(uint256 ibgtAmount) internal {
    ERC20(ibgt).approve(ibgtVault, ibgtAmount);
    iBGTVault(ibgtVault).stake(ibgtAmount); //@audit will revert here
  }
```

**Impact:** Users can't lock `iBGT` as `lock()` always reverts.

**Recommended Mitigation:** `_refreshiBGT()` should be called after pulling funds from the user.

**Client:** Fixed in [PR #1](https://github.com/0xgeeb/goldilocks-core/pull/1)

**Cyfrin:** Verified.
