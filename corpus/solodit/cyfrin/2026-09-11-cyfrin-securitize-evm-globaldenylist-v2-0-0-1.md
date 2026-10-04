---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-0-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`ComplianceServicePermissionless::checkTransfer` never screens the `transferFrom`
  spender, so denylisted address can direct transfers of other wallets'' tokens breaching
  OFAC FAQ400 compliance'
vuln_class: []
---

# `ComplianceServicePermissionless::checkTransfer` never screens the `transferFrom` spender, so denylisted address can direct transfers of other wallets' tokens breaching OFAC FAQ400 compliance

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `DSToken::transferFrom` applies the `canTransfer` modifier, which forwards only the token owner and the recipient into `validateTransfer`. `msg.sender`, the spender exercising the allowance, never reaches the compliance layer, so `ComplianceServicePermissionless::checkTransfer` evaluates the denylist against `_from` and `_to` only.

A globally denylisted address holding an allowance from a clean owner can therefore call `transferFrom` and move that owner's tokens to a clean recipient. `DSToken::approve` carries no compliance check either, so an allowance can also be granted to an address after it has been denylisted.

**Impact:** No value flows to or from the denylisted address, so this is not an asset-recovery bypass. Rather is in breach of OFAC compliance; [OFAC FAQ 400](https://ofac.treasury.gov/faqs/400) explicitly forbids sanctioned entities from directing transactions:

> Can persons engage in negotiations, enter into contracts, or process transactions involving a blocked individual when that blocked individual is acting on behalf of the non-blocked entity that he or she controls...
>
> No. OFAC sanctions generally prohibit transactions involving, directly or indirectly, a blocked person, absent authorization from OFAC, even if the blocked person is acting on behalf of a non-blocked entity.

[OFAC's virtual-currency guidance](https://ofac.treasury.gov/media/913571/download?inline) confirms the obligations apply identically on-chain, and FAQ 560 states compliance obligations are the same regardless of whether a transaction is denominated in digital or fiat currency.

A wallet-level control screening only the two ends of the value flow cannot express the FAQ 400 prohibition. If the shared denylist is intended to carry sanctions listings, an OFAC sanctioned address can still act as an authorized agent over other holders' tokens on every wired token.

The likelier subject is a contract rather than an individual: denylisting a sanctioned protocol or venue address stops it holding or receiving tokens, but not pulling tokens from every wallet that already approved it.

**Recommended Mitigation:** * Screen the spender on the paths where a spender exists, not inside `checkTransfer`. `checkTransfer` is reached by `preTransferCheck`, an off-chain view whose `msg.sender` is the arbitrary caller of the view and carries no meaning there:

```diff
function transferFrom(address _from, address _to, uint256 _value)
    public virtual override canTransfer(_from, _to, _value) returns (bool)
{
+   require(!getComplianceService().isGloballyDenylistedWallet(msg.sender), "Spender is globally denylisted");
    return postTransferImpl(super.transferFrom(_from, _to, _value), _from, _to, _value);
}
```

* the above check automatically applies to `transferWithPermit`, but also consider whether `approve` and the allowance-increase functions should also reject a denylisted spender, so fresh authority cannot be granted to an OFAC designated address after listing

* Have `GlobalDenyListManager::isGloballyDenylisted` additionally call [0x40C57923924B5c5c5455c48D93317139ADDaC8fb::isSanctioned(address)](https://etherscan.io/address/0x40C57923924B5c5c5455c48D93317139ADDaC8fb#readContract#F1) to easily reject transfers involving OFAC sanctioned entities without needing to maintain a duplicated list

* Consider adding a function `GlobalDenyListManager::isGloballyDenylisted(address[] calldata wallets)` such that callers can make only one external call to check a list of input addresses. For example when checking a token transfer, one external call could be made to check `spender, from, to` which is more efficient than making 3 external calls

If it is by design that spender bypasses the deny list breaching OFAC compliance, this should be explicitly documented since the omission is otherwise indistinguishable from an oversight.

**Securitize:** Fixed in commits [4e0b2dd](https://github.com/securitize-io/dstoken/commit/4e0b2dd50b81f9faa0ecae60a30cf6317bf2a035), [a6852ab](https://github.com/securitize-io/dstoken/commit/a6852abdeb1f1f3bd9a8e29ea061e6766543bf19) and added bulk deny list check in commit [a96f979](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/a96f979db4206c4cc26f5029b893debead847604).

**Cyfrin:** Verified.
