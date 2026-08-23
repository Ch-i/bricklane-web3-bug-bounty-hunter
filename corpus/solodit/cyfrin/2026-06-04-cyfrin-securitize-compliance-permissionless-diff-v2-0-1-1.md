---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2-0
title: '`WalletManager::setSpecialWallet` guard is inert under the stub registry,
  letting an Issuer label any token-holding wallet as a platform wallet and bypass
  an active lockup'
vuln_class: []
---

# `WalletManager::setSpecialWallet` guard is inert under the stub registry, letting an Issuer label any token-holding wallet as a platform wallet and bypass an active lockup

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-04-cyfrin-securitize-compliance-permissionless-diff-v2.0.md)_

---

**Description:** `WalletManager:setSpecialWallet` carries a defense intended to stop a wallet that belongs to a registered investor from being labeled a "special" (platform / issuer / exchange) wallet — special wallets receive compliance exemptions, so labeling an investor's wallet would let it escape those rules:

```solidity
// compliance/WalletManager.sol
function setSpecialWallet(address _wallet, uint8 _type) internal override returns (bool) {
    require(CommonUtils.isEmptyString(getRegistryService().getInvestor(_wallet)), "Wallet belongs to investor"); // @audit always passes under the stub
    ...
    walletsTypes[_wallet] = _type;
    ...
}

function addPlatformWallet(address _wallet) public override onlyIssuerOrAbove returns (bool) {
    return setSpecialWallet(_wallet, PLATFORM);
}
```

Under `StubRegistryService`, `getInvestor(addr)` returns `""` for every address, so `isEmptyString(...)` is always `true` and the `require` never blocks. The guard is structurally inert in the permissionless configuration.

Platform wallets are exempt from the lockup in `ComplianceServicePermissionless:newPreTransferCheck`:

```solidity
// compliance/ComplianceServicePermissionless.sol
if (!getWalletManager().isPlatformWallet(_from)) {           // @audit platform wallets skip the lockup check
    uint256 locked = _lockedAt(_from, block.timestamp);
    if (locked > 0 && _value > _balanceFrom - locked) {
        return (16, TOKENS_LOCKED);
    }
}
```

Consequently an `onlyIssuerOrAbove` caller can take any wallet that currently holds locked tokens, call `addPlatformWallet(thatWallet)` — which always succeeds under the stub — and the wallet's lockup is immediately bypassed: transfers from it stop returning code 16.

**Impact:** An Issuer can exempt any wallet from the lockup by labeling it a platform wallet, defeating the lockup for that address. The lockup is itself an Issuer/Transfer-Agent-configurable compliance feature, and no funds are lost — only the lockup timing guarantee for the affected wallet is removed.

**Recommended Mitigation:** Consider reverting the labeling of a wallet as `PLATFORM` while it has an active lockup.

**Securitize:** Fixed in [0ede206](https://github.com/securitize-io/dstoken/commit/0ede2064de4e430eb8cc182f29e97e78550b2a7a).

**Cyfrin:**
Verified. Labeling a wallet as platform no longer bypasses active lockup records, since transfer-time lock checks now apply to platform wallets as well.

\clearpage
