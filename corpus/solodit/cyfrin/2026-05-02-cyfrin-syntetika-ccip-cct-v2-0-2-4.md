---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Minter::mint` docstring vs code: recipient is never checked against whitelist'
vuln_class: []
---

# `Minter::mint` docstring vs code: recipient is never checked against whitelist

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The NatSpec for `Minter::mint` states:

> `@dev Requires both sender and recipient to be whitelisted.`

The implementation applies only `onlyWhitelisted(msg.sender)`:

```solidity
function mint(
    address to,
    uint256 amount
) external onlyWhitelisted(msg.sender) nonReentrant whenNotPaused {
    MinterStorage storage $ = _getMinterStorage();
    $.baseAsset.safeTransferFrom(msg.sender, address(this), amount);
    $.hilSyntheticToken.mint(to, amount);        // ← to is never checked
    $.totalDeposits += amount;
    emit Minted(to, amount);
}
```

`onlyWhitelisted` either fast-paths for a manually whitelisted address or runs `PolicyEngine.run()` for non-whitelisted callers. The modifier is called once, with `msg.sender`. The `to` parameter is never passed to `onlyWhitelisted` or any equivalent compliance gate. `HilToken::_update` subsequently checks only the `_blacklisted` mapping (not the whitelist) for `from`, `to`, and `msg.sender` — so minting to a non-blacklisted, non-whitelisted address succeeds without triggering any compliance check.

A whitelisted caller can therefore:
1. Call `Minter::mint(nonCompliantAddress, amount)` — depositing `baseAsset` and receiving `amount` HilBTC/HilUSD credited to `nonCompliantAddress`.
2. `nonCompliantAddress` now holds regulated synthetic assets despite never being screened by the whitelist or PolicyEngine.

The `onlyWhitelisted` check on transfers via `HilToken::requestTransfer` / `_update` is the only downstream gate, but it applies to *transfers*, not to the initial mint — so tokens land in a non-compliant wallet before any transfer-time checks can fire.

**Impact:**
- Synthetic HilBTC/HilUSD can be issued to wallets that have not undergone any KYC/AML screening, directly contradicting the protocol's stated compliance model.
- A whitelisted user (e.g., one institution's trader) can mint or transfer to an arbitrary counterparty without that counterparty satisfying any onboarding requirement.
- Depending on regulatory context, issuance of regulated synthetic assets to unscreened recipients may expose the protocol operator to compliance liability independent of technical severity.

**Mitigation:**

Add `onlyWhitelisted(to)` to `Minter::mint` alongside the existing `onlyWhitelisted(msg.sender)` check:

```solidity
function mint(
    address to,
    uint256 amount
) external onlyWhitelisted(msg.sender) onlyWhitelisted(to) nonReentrant whenNotPaused {
```

Alternatively, add an explicit `require(isAddressWhitelisted(to) || policyCheck(to), RecipientNotCompliant())` if the `onlyWhitelisted` double-modifier approach conflicts with gas or PolicyEngine assumptions.

Additionally, implement whitelist checks in `HilToken::_update` to disallow transfers to non-whitelisted users.

**Syntetika:** Fixed in commit [`38c2f5c`](https://github.com/SyntetikaLabs/monorepo/commit/38c2f5ca16e3065b59f2114c38e665d90c9e5ff9): Whitelist required only for minting - transferring should without wl restriction.

**Cyfrin:** Verified. Comment changed to remove mentioning whitelisting.
