---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-3-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Self reassignment temporarily hides claims from aggregate indexes until administrator
  repair
vuln_class: []
---

# Self reassignment temporarily hides claims from aggregate indexes until administrator repair

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** Calling either claimable-balance reassignment function with the same source and destination preserves the controller's per-generation balance while removing the generation from the index used by every aggregate claim path. The affected controller cannot claim the deposit or redemption through the aggregate paths until an administrator repairs the index, and a redemption leaves its committed liquidity locked during that interval.

`AsyncFundVaultAdmin::reassignClaimableDeposit` does not reject `from == to`. When both arguments identify the same controller, `toHadNoPriorClaim` is false because the controller already has a nonzero balance. The function then clears and restores the same mapping slot, removes the generation from `controllerDepositGenerations`, and does not add it back. `AsyncFundVaultAdmin::reassignClaimableRedemption` repeats the same sequence for redemption claims.

```solidity
// contracts/base/AsyncFundVaultAdmin.sol:242-266
function reassignClaimableDeposit(uint256 generationId, address from, address to)
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
{
    if (to == address(0)) revert ZeroAddress();

    VaultStorage storage $ = _getStorage();

    if ($.depositGenerations[generationId].status != GenerationStatus.Fulfilled) {
        revert GenerationNotFulfilled(generationId);
    }

    uint256 amount = $.pendingDepositAssets[generationId][from];
    if (amount == 0) revert NoRequestInGeneration(generationId, from);

    bool toHadNoPriorClaim = $.pendingDepositAssets[generationId][to] == 0;
    $.pendingDepositAssets[generationId][from] = 0;
    $.pendingDepositAssets[generationId][to] += amount;

    _removeFromList($.controllerDepositGenerations[from], generationId);
    if (toHadNoPriorClaim) {
        $.controllerDepositGenerations[to].push(generationId);
    }
}

// contracts/base/AsyncFundVaultAdmin.sol:272-294
function reassignClaimableRedemption(uint256 generationId, address from, address to)
    external
    onlyRole(DEFAULT_ADMIN_ROLE)
{
    if (to == address(0)) revert ZeroAddress();

    VaultStorage storage $ = _getStorage();

    if ($.redeemGenerations[generationId].status != GenerationStatus.Fulfilled) {
        revert GenerationNotFulfilled(generationId);
    }

    uint256 shares = $.pendingRedeemShares[generationId][from];
    if (shares == 0) revert NoRequestInGeneration(generationId, from);

    bool toHadNoPriorClaim = $.pendingRedeemShares[generationId][to] == 0;
    $.pendingRedeemShares[generationId][from] = 0;
    $.pendingRedeemShares[generationId][to] += shares;

    _removeFromList($.controllerRedeemGenerations[from], generationId);
    if (toHadNoPriorClaim) {
        $.controllerRedeemGenerations[to].push(generationId);
    }
}
```

The direct request views continue to read the nonzero mapping entries. In contrast, `AsyncFundVault::_computeClaimableDepositTotals` and `AsyncFundVault::_computeClaimableRedemptionTotals` enumerate only the corresponding controller generation arrays. Once self-reassignment removes the generation, `AsyncFundVault::deposit`, `AsyncFundVault::mint`, `AsyncFundVault::redeem`, and `AsyncFundVault::withdraw` all observe zero aggregate claimable value and revert before clearing the request.

```solidity
// contracts/AsyncFundVault.sol:832-848
uint256[] storage genIds = $.controllerDepositGenerations[controller];
uint256 len = genIds.length;
for (uint256 i; i < len; ++i) {
    uint256 genId = genIds[i];
    uint256 amount = $.pendingDepositAssets[genId][controller];
    if (amount > 0 && $.depositGenerations[genId].status == GenerationStatus.Fulfilled) {
        claimedAssets += amount;
        claimedShares += _assetsToShares(
            amount,
            $.depositGenerations[genId].navPrice,
            $.dsDecimals,
            $.liquidityDecimals
        );
    }
}

// contracts/AsyncFundVault.sol:875-892
uint256[] storage genIds = $.controllerRedeemGenerations[controller];
uint256 len = genIds.length;
for (uint256 i; i < len; ++i) {
    uint256 genId = genIds[i];
    uint256 amount = $.pendingRedeemShares[genId][controller];
    if (amount > 0 && $.redeemGenerations[genId].status == GenerationStatus.Fulfilled) {
        RedemptionGenerationData storage gen = $.redeemGenerations[genId];
        totalShares += amount;
        totalLiquidity += (amount * gen.totalLiquidity) / gen.totalPendingShares;
    }
}
```

**Impact:** Self-reassignment can hide an otherwise valid deposit or redemption claim from aggregate lookup and continue reserving associated liquidity. Only `DEFAULT_ADMIN_ROLE` can trigger and repair the inconsistency, so it is an operationally induced temporary denial of claim access rather than an unprivileged exploit.


**Recommended Mitigation:** Reject `from == to` with a dedicated error in both reassignment functions before mutating balances or indexes, preserving the mapping-to-index invariant and surfacing operator mistakes.

**Securitize:** Fixed in commit [7999a4f](https://github.com/securitize-io/bc-async-ramp-sc/commit/7999a4f1966cd6746f78d2e8aea0a1435735e262).

**Cyfrin:** Verified.
