---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Check return value when calling `Allowlist::exchangeAllowed` and `RemoraToken::_exchangeAllowed`
  to prevent unauthorized transfers
vuln_class: []
---

# Check return value when calling `Allowlist::exchangeAllowed` and `RemoraToken::_exchangeAllowed` to prevent unauthorized transfers

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `Allowlist::exchangeAllowed` will revert if the users are not allowed but when the users are both allowed, it will return a boolean determined by whether the `domestic` field of both users match:
```solidity
function exchangeAllowed(
    address from,
    address to
) external view returns (bool) {
    HolderInfo memory fromUser = _allowed[from];
    HolderInfo memory toUser = _allowed[to];
    if (from != address(0) && !fromUser.allowed)
        revert UserNotRegistered(from);
    if (to != address(0) && !toUser.allowed) revert UserNotRegistered(to);
    return fromUser.domestic == toUser.domestic; //logic to be edited later on
}
```

But `RemoraToken::adminTransferFrom` doesn't check the boolean return when calling `Allowlist::exchangeAllowed`:
```solidity
function adminTransferFrom(
    address from,
    address to,
    uint256 value,
    bool checkTC,
    bool enforceLock
) external restricted returns (bool) {
    // @audit boolean return not checked
    IAllowlist(allowlist).exchangeAllowed(from, to);
```

Similary `RemoraToken::_exchangeAllowed` returns the boolean output of `Allowlist::exchangeAllowed`, but this is never checked in `RemoraToken::transfer`, `transferFrom`.

**Impact:** Transfers are allowed even when `Allowlist::exchangeAllowed` returns `false`.

**Recommended Mitigation:** Check the boolean return of `Allowlist::exchangeAllowed`, `RemoraToken::_exchangeAllowed` and only allow transfers when they return `true`.

Alternatively change `Allowlist::exchangeAllowed` and `RemoraToken::_exchangeAllowed` to not return anything but to always revert.

**Remora:** Fixed in commit [13cf261](https://github.com/remora-projects/remora-smart-contracts/commit/13cf261d37f5756cac480aa1e0c8ecf756fd3af5).

**Cyfrin:** Verified.
