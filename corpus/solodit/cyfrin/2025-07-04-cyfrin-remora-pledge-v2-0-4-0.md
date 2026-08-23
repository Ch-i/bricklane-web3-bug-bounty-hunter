---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Fail fast without performing unnecessary storage reads
vuln_class: []
---

# Fail fast without performing unnecessary storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Fail fast without performing unnecessary storage reads:

* `Allowlist::exchangeAllowed` - don't read `_allowed[to]` from storage if the transaction will fail since `from` is not allowed:
```solidity
    function exchangeAllowed(
        address from,
        address to
    ) external view returns (bool) {
        HolderInfo memory fromUser = _allowed[from];
        if (from != address(0) && !fromUser.allowed) revert UserNotRegistered(from);

        HolderInfo memory toUser = _allowed[to];
        if (to != address(0) && !toUser.allowed) revert UserNotRegistered(to);

        return fromUser.domestic == toUser.domestic; //logic to be edited later on
    }
```

* `Allowlist::hasTradeRestriction` - don't read `_allowed[user2]` from storage if the transaction will fail since `_allowed[user1]` is not allowed:
```solidity
    function hasTradeRestriction(
        address user1,
        address user2
    ) public returns (bool) {
        HolderInfo memory u1Data = _allowed[user1];
        if (!u1Data.allowed) revert UserNotRegistered(user1);

        HolderInfo memory u2Data = _allowed[user2];
        if (!u2Data.allowed) revert UserNotRegistered(user2);
```

**Remora:** Fixed in commits [81faadb](https://github.com/remora-projects/remora-smart-contracts/commit/81faadbd3baa1deec950db08abf635c5a277a7c5), [760469f](https://github.com/remora-projects/remora-smart-contracts/commit/760469fb5a0263ab5527d7c35e7887349f1a2368).

**Cyfrin:** Verified.
