---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-5-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Storage read optimizations
vuln_class: []
---

# Storage read optimizations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:**
1. [`AccountableOpenTerm::_calculateRequiredLiquidity`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L642-L655): `vault` and `_scaleFactor` can be cached. Also consider changing so that `_calculateRequiredLiquidity` takes `address vault_` as a parameter. That would allow to cache the   `vault` read in the [`_isDelinquent`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L492-L497), [`_getAvailableLiquidity`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L658-L663), [`_borrowable`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L518-L523) and [`_validateLiquidityForTermChange`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L526-L533) flows as well.

2. [`AccountableOpenTerm::_getAvailableLiquidityForProcessing`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L666-L671): `vault` can be cached. Also consider same as above, add `address vault_` as a parameter, then use a cached value from [`_processAvailableWithdrawals`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L536-L570).

3. [`AccountableOpenTerm::_penaltyFee`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L587-L599), use the cached value `gracePeriod` on [L595](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L595)

4. [`AccountableOpenTerm::supply`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L238-L244): `vault` can be cached

5. [`AccountableOpenTerm::repay`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableOpenTerm.sol#L260-L272): `vault` can be cached.

6. [`AccountableFixedTerm::_sharePrice`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableFixedTerm.sol#L533-L540): `loanState` can be cached.

7. [`AccountableStrategy::acceptBorrowerRole`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableStrategy.sol#L181-L189): Use `msg.sender` instead of `pendingBorrower` on [L185](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableStrategy.sol#L185) and instead of `borrower` on [L188](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableStrategy.sol#L188)

8. [`AccountableStrategy::_requireLoanNotOngoing`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableStrategy.sol#L474-L476): `loanState` can be cached.

9. [`AccountableStrategy::_requireLoanOngoing`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/strategies/AccountableStrategy.sol#L479-L481): `loanState` can be cached.

10. [AccountableWithdrawalQueue::_push](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/queue/AccountableWithdrawalQueue.sol#L82-L84): Set `_queue.nextRequestId` to `1` at construction and remove the if to save a read each `_push`.

11. [`AccountableAsyncRedeemVault::redeem`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L155-L156): `state.redeemPrice` can be cached

12. [`AccountableAsyncRedeemVault::withdraw`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L176-L177): `state.withdrawPrice` can be cached.

13. [`AccountableAsyncRedeemVault::_updateRedeemState`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L197-L201): `state.maxWithdraw` and `state.redeemShares` can be cached.

14. [`AccountableAsyncRedeemVault::_fulfillRedeemRequest`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L305-L326): `state.pendingRedeemRequest`, `state.maxWithdraw` and `state.redeemShares` can be cached.

15. [`AccountableAsyncRedeemVault::maxRedeem`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L352-L356) and [AccountableAsyncRedeemVault::maxWithdraw](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/vault/AccountableAsyncRedeemVault.sol#L359-L363): Can be rewritten as:
    ```solidity
    function maxWithdraw(address receiver) public view override returns (uint256 maxAssets) {
        VaultState storage state = _vaultStates[receiver];
        maxAssets = state.maxWithdraw;
        if (state.redeemShares == 0) return 0;
    }
    ```

16. [`Authorizable::_verify`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/access/Authorizable.sol#L47-L75): `signer` can be cached.

17. [`RewardsDistributorMerkle::acceptRoot`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/rewards/RewardsDistributorMerkle.sol#L67-L68): `_pendingRoot.validAt` can be cached.

18. [`RewardsDistributorMerkle::claim`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/rewards/RewardsDistributorMerkle.sol#L100-L102): `claimed[account][asset])` can be cached

19. [`RewardsDistributorStrategy::claim`](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/rewards/RewardsDistributorStrategy.sol#L40-L42): `claimed[account][asset])` can be cached


**Accountable:** Most fixed in commit [`8e1cfa2`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/8e1cfa29de4dc4b0198e26e59acb56e7c929dbcf)

**Cyfrin:** Verified.

\clearpage
