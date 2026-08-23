---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-0-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: '`ComplianceServiceGlobalWhitelisted::newPreTransferCheck` and `preTransferCheck`
  allow blacklisted users to transfer tokens'
vuln_class: []
---

# `ComplianceServiceGlobalWhitelisted::newPreTransferCheck` and `preTransferCheck` allow blacklisted users to transfer tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `ComplianceServiceGlobalWhitelisted::newPreTransferCheck` and `preTransferCheck` only enforce that the recipient of tokens is not blacklisted, but they don't check that the sender is also not blacklisted:
```solidity
function newPreTransferCheck(
    address _from,
    address _to,
    uint256 _value,
    uint256 _balanceFrom,
    bool _pausedToken
) public view virtual override returns (uint256 code, string memory reason) {
    // First check if recipient is blacklisted
    if (getBlackListManager().isBlacklisted(_to)) {
        return (100, WALLET_BLACKLISTED);
    }

    // Then perform the standard whitelist check
    return super.newPreTransferCheck(_from, _to, _value, _balanceFrom, _pausedToken);
}

function preTransferCheck(address _from, address _to, uint256 _value) public view virtual override returns (uint256 code, string memory reason) {
    // First check if recipient is blacklisted
    if (getBlackListManager().isBlacklisted(_to)) {
        return (100, WALLET_BLACKLISTED);
    }

    // Then perform the standard whitelist check
    return super.preTransferCheck(_from, _to, _value);
}
```

**Impact:** A blacklisted user can transfer their tokens to a non-blacklisted user, effectively evading the blacklist.

**Recommended Mitigation:** `ComplianceServiceGlobalWhitelisted::newPreTransferCheck` and `preTransferCheck` should return correct error codes if `from` address is blacklisted.

**Securitize:** Fixed in commits [32d1a02](https://github.com/securitize-io/dstoken/commit/32d1a020f4fad010f656da2a0da739b06d338e65), [a616d39](https://github.com/securitize-io/dstoken/commit/a616d398add96a08e53942a11ba26cfc505a8ef3).

**Cyfrin:** Verified.
