---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-6
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: ERC 7540 and ERC 7575 conformance gaps break standard discovery and claim availability
  views
vuln_class: []
---

# ERC 7540 and ERC 7575 conformance gaps break standard discovery and claim availability views

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** The vault advertises conformance with ERC-7540, but its request identifiers, interface discovery, share token lookup, and maximum claim views do not implement several requirements of the final standard. Generic ERC-7540 routers and indexers can consequently reject the vault, misclassify requests, or conclude that a valid claim is unavailable.

The first deposit and redemption generations both receive identifier zero because each counter starts at zero and is incremented after assignment. Later generations return nonzero identifiers. ERC-7540 specifies that once a vault returns zero for any request identifier, it must return zero for every request. The vault instead changes identifier models after its first generation.

```solidity
// contracts/AsyncFundVault.sol:270-272
generationId = $.depositGenerationCount++;
$.depositGenerations[generationId].status = GenerationStatus.Active;
$.currentDepositGenerationId = generationId;

// contracts/AsyncFundVault.sol:327-329
generationId = $.redeemGenerationCount++;
$.redeemGenerations[generationId].status = GenerationStatus.Active;
$.currentRedeemGenerationId = generationId;
```

The final ERC-7540 specification also requires ERC-165 discovery for the operator, deposit request, redemption request, and ERC-7575 interfaces. It requires ERC-7575 support, in particular a nonreverting `IERC7575::share` function that returns the external DS Token address. `AsyncFundVault` does not define `IERC7575::share`, and its inherited `AsyncFundVault::supportsInterface` implementation does not return the required identifiers. The normative requirements are documented at https://eips.ethereum.org/EIPS/eip-7540 and https://eips.ethereum.org/EIPS/eip-7575.

Finally, the maximum functions describe request intake or return fixed zero values instead of exposing the caller's claimable state. ERC-7540 uses the existing ERC-4626 functions as claim entry points and states that `IERC4626::maxDeposit` increases and decreases with `IERC7540::claimableDepositRequest`. `AsyncFundVault::maxDeposit` returns `type(uint256).max` whenever subscriptions are open, even when the queried controller has no claimable deposit, while `AsyncFundVault::maxWithdraw` and `AsyncFundVault::maxRedeem` return zero even when the controller has a fulfilled redemption.

```solidity
// contracts/AsyncFundVault.sol:192-212
function maxDeposit(address /* receiver */ ) external view returns (uint256) {
    VaultStorage storage $ = _getStorage();
    return ($.subscriptionsEnabled && !paused()) ? type(uint256).max : 0;
}

function maxMint(address /* receiver */ ) external view returns (uint256) {
    VaultStorage storage $ = _getStorage();
    return ($.subscriptionsEnabled && !paused()) ? type(uint256).max : 0;
}

function maxWithdraw(address /* owner */ ) external pure returns (uint256) {
    return 0;
}

function maxRedeem(address /* owner */ ) external pure returns (uint256) {
    return 0;
}
```

**Impact:** Standards-aware integrations may fail to discover the asynchronous interfaces, resolve the DS Token through `share()`, or determine claim availability from the `max*` functions. Mixed request-ID semantics can also cause indexers to merge or mislabel requests; protocol-specific users can still transact, so the primary impact is failed or omitted integration activity rather than direct asset loss.


**Recommended Mitigation:** Use one ERC-7540 request-ID model consistently, implement ERC-7575 `share()`, and report all required interface IDs through `supportsInterface`. Make `maxDeposit`, `maxMint`, `maxWithdraw`, and `maxRedeem` reflect each controller's currently claimable amounts.

**Securitize:** Fixed in commit [20461a7](https://github.com/securitize-io/bc-async-ramp-sc/commit/20461a787298777e178d08f1cf34f98b2bdc7f66).

**Cyfrin:** Verified.
