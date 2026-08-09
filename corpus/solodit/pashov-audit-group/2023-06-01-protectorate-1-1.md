---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[H-02] Vault depositors can be front-ran and lose their funds'
vuln_class: []
---

# [H-02] Vault depositors can be front-ran and lose their funds

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

**Impact:**
High, as a theft of user assets is possible

**Likelihood:**
Medium, as it works only if the attacker is the first vault depositor

**Description**

The following attack is possible:

1. The `LendingVault` contract has just been deployed and has 0 `assets` and `shares` deposited/minted
2. Alice sends a transaction to deposit `10e18` worth of `_assets`
3. Bob is a malicious user/bot and sees the transaction in the mempool and front-runs it by depositing 1 wei worth of the asset, receiving 1 wei of shares
4. Bob also front-runs Alice's transaction with a direct ERC20::transfer of 10e18 worth of the asset to the `LendingVault` contract
5. Now in Alice's transaction, the code calculates Alice's shares as `shares = assets.mulDiv(totalSupply(), totalAssets(), Math.Rounding.Down)` where the `totalAssets` returns `_asset.balanceOf(address(this))` which makes shares round down to 0
6. Alice gets minted 0 shares, even though she deposited 10e18 worth of the asset
7. Now Bob back-runs Alice's transaction with a call to ` withdraw`` where  `assets` is the contract's balance of the asset, allowing him to burn his 1 share and withdraw his deposit + Alice's whole deposit

This can be replayed multiple times until the depositors notice the problem.

**Recommendations**

First, make sure that all deposits will go through Flashbots so the transactions are not sandwhichable/front-runnable.

Then we can look at how UniswapV2 fixed this with two types of protection:

[First](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L119-L121), on the first `mint` it actually mints the first 1000 shares to the zero-address

[Second](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol#L125), it requires that the minted shares are not 0

Implementing all of those solutions will resolve this vulnerability.
