---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: The vault limit condition should not be checked for `address(0)`
vuln_class: []
---

# The vault limit condition should not be checked for `address(0)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The virtual function `ERC721Upgradeable::_update` has been overridden within `SmartVaultManagerV6` as follows:

```solidity
function _update(address _to, uint256 _tokenID, address _auth) internal virtual override returns (address) {
    address _from = super._update(_to, _tokenID, _auth);
    require(vaultIDs(_to).length < userVaultLimit, "err-vault-limit");
    smartVaultIndex.transferTokenId(_from, _to, _tokenID);
    if (address(_from) != address(0)) ISmartVault(smartVaultIndex.getVaultAddress(_tokenID)).setOwner(_to);
    emit VaultTransferred(_tokenID, _from, _to);
    return _from;
}
```

However, the `userVaultLimit` validation should not be performed for `address(0)` otherwise it will become impossible to burn more than this number of tokens. Fortunately, such functionality is not currently exposed and it is not possible to transfer tokens directly to `address(0)` due to do validation within the OpenZeppelin contract. Nevertheless, this edge case should be proactively avoided.

Similarly, the call to `SmartVaultIndex::removeTokenId` within `SmartVaultIndex::transferTokenId` should be skipped if the `_from` is `address(0)` and pushing to the `tokenIds` array should be skipped if `_to` is `address(0)`:

```solidity
function transferTokenId(address _from, address _to, uint256 _tokenId) external onlyManager {
    removeTokenId(_from, _tokenId);
    tokenIds[_to].push(_tokenId);
}
```

**The Standard DAO:** Fixed by commit [ff4ef5b](https://github.com/the-standard/smart-vault/commit/ff4ef5b85561daf24f0443079a570f4bf4bd7389).

**Cyfrin:** Verified. The validation will now pass for the zero address.
