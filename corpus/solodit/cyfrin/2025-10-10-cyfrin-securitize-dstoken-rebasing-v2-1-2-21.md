---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-21
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Resolve inconsistency between `DSToken::checkWalletsForList` and `RegistryService::removeWallet`
vuln_class: []
---

# Resolve inconsistency between `DSToken::checkWalletsForList` and `RegistryService::removeWallet`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `DSToken::checkWalletsForList` only removes wallets if their balance is zero:
```solidity
function checkWalletsForList(address _from, address _to) private {
    if (super.balanceOf(_from) == 0) {
        removeWalletFromList(_from);
    }
```

But `RegistryService::removeWallet` allows removing wallets with positive balances:
```solidity
function removeWallet(address _address, string memory _id) public override onlyExchangeOrAbove walletExists(_address) walletBelongsToInvestor(_address, _id) returns (bool) {
    require(getTrustService().getRole(msg.sender) != EXCHANGE || investorsWallets[_address].creator == msg.sender, "Insufficient permissions");

    delete investorsWallets[_address];
    investors[_id].walletCount--;

    emit DSRegistryServiceWalletRemoved(_address, _id, msg.sender);

    return true;
}
```

**Impact:** Wallets with positive balances can be removed via `RegistryService::removeWallet` which prevents token transfers and other related activity that depends on functions from `RegistryService` returning investor ids for given wallet addresses.

**Recommended Mitigation:** `RegistryService::removeWallet` shouldn't allow removing wallets with positive balances.

**Securitize:** Fixed in commit [1eaec18](https://github.com/securitize-io/dstoken/commit/1eaec18ce4a9dc6be24c43d02950839341b6282d#diff-8abf57cc60f7fc1ff193a0912746e8539f56be2d652f1bb59fa5ea8ef3c43d97R177-R178).

**Cyfrin:** Verified.
