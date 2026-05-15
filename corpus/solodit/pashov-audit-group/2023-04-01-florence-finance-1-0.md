---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[H-01] Stakers/vault depositors can be front-run and lose their funds'
vuln_class: []
---

# [H-01] Stakers/vault depositors can be front-run and lose their funds

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as it results in a theft of user assets

**Likelihood:**
Medium, as it works only if the attacker is the first staker

**Description**

Let's look at the following example:

1. The `FlorinStaking` contract has been deployed, unpaused and has 0 staked $FLR in it
2. Alice sends a transaction calling the `stake` method with `florinTokens == 10e18`
3. Bob is a malicious user/bot and sees the transaction in the mempool and front-runs it by depositing 1 wei of $FLR, receiving 1 wei of shares
4. Bob also front-runs Alice's transaction with a direct `ERC20::transfer` of 10e18 $FLR to the `FlorinStaking` contract
5. Now in Alice's transaction, the code calculates Alice's shares as `shares = florinTokens.mulDiv(totalShares_, getTotalStakedFlorinTokens(), MathUpgradeable.Rounding.Down);`, where `getTotalStakedFlorinTokens` returns `florinToken.balanceOf(address(this))`, so now `shares` rounds down to 0
6. Alice gets minted 0 shares, even though she deposited 10e18 worth of $FLR
7. Now Bob back-runs Alice's transaction with a call to `unstake` where `requestedFlorinTokens` is the contract's balance of $FLR, allowing him to burn his 1 share and withdraw his deposit + Alice's whole deposit

This can be replayed multiple times until the depositors notice the problem.

**Note:** This absolute same problem is present with the ERC4626 logic in `LoanVault`, as it is a common vulnerability related to vault shares calculations. OpenZeppelin has introduced a way for mitigation in version 4.8.0 which is the used version by this protocol.

**Recommendations**

UniswapV2 fixed this with two types of protection:

[First](https://github.com/Uniswap/v2-core/blob/master/contracts/UniswapV2Pair.sol#L119-L121), on the first `mint` it actually mints the first 1000 shares to the zero-address

[Second](https://github.com/Uniswap/v2-core/blob/ee547b17853e71ed4e0101ccfd52e70d5acded58/contracts/UniswapV2Pair.sol#L125), it requires that the minted shares are not 0

Implementing them both will resolve this vulnerability.
