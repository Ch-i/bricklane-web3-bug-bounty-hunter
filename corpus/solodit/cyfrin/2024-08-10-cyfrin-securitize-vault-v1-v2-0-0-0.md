---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-10-cyfrin-securitize-vault-v1-v2-0-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-10T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-10-cyfrin-securitize-vault-v1-v2-0
title: Incomplete access control over deposit and redeem
vuln_class: []
---

# Incomplete access control over deposit and redeem

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-10-cyfrin-securitize-vault-v1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-10-cyfrin-securitize-vault-v1-v2.0.md)_

---

**Description:** `SecuritizeVault` was designed to limit access to deposit and redeem but due to missed overrides it is still possible to use the access-controlled functions.
The vault contract inheritied the OpenZeppelin's `ERC4626Upgradeable` and `ERC4626Upgradeable` has several public functions exposed by default. Especially, `ERC4626Upgradeable` allows mint/deposit and redeem/withdraw in two ways.
```solidity
function deposit(uint256 assets, address receiver) public virtual returns (uint256);
function mint(uint256 shares, address receiver) public virtual returns (uint256);

function withdraw(uint256 assets, address receiver, address owner) public virtual returns (uint256);
function redeem(uint256 shares, address receiver, address owner) public virtual returns (uint256);
```
Note that `deposit()` and `withdraw()` functions accept the asset amount while `mint()` and `redeem()` functions accept the share amount as parameters.

`SecuritizeVault` has overriden the function `deposit()` and `redeem()` with additional access controls.
For the function `deposit()`, the vault only allowed depositing to itself and for the function `redeem()` the vault allowed only redeemers.
But because the vault did not override the other functions `mint()` and `withdraw()`, it is still possible to work around this limitation.

Moreover, deposit and redeem will be possible even when the vault is paused by the owner.

**Impact:** Access control is broken and anyone can deposit to any other address and anyone can redeem while it is not the protocol's intention.
Furthermore, deposit and redeem will function even when the vault contract is paused by the owner.
We evaluate the impact to be CRITICAL.

**Proof Of Concept:**
Put the test inside `deposit.test.ts`.
```typescript
    it('Cyfrin: Can deposit using a mint function even if receiver is not the same as sender', async () => {
      const { vault, dsMock, redeemer, owner } = await loadFixture(deployRedemptionVault);
      await dsMock.mint(owner.address, amount);
      await dsMock.approve(vault.target, amount);

      console.log(await vault.balanceOf(redeemer.address));
      await vault.mint(amount, redeemer.address);
      console.log(await vault.balanceOf(redeemer.address));
    });
```
**Recommended Mitigation:**
- Override the other functions `mint()` and `withdraw()` with the same access control.
- Note that `deposit()` and `redeem()` is not an ideal pair to be implemented and exposed. In general, it is either deposit and withdraw, or mint and redeem.
- Note that the modifier `receiverSenderNotEqual(receiver)` is technically not meaningful because anyone can transfer the shares (vault token) to others.

**Securitize:** Fixed in Commit [52350aa](https://bitbucket.org/securitize_dev/bc-securitize-vault-sc/commits/52350aa809c140edc6f794baabc7e53891b37852).

**Cyfrin:** Verified.
- Public functions `mint()` and `withdraw()` are overridden to revert all the time.
- The modifier `receiverSenderNotEqual(receiver)` has been removed.

\clearpage
