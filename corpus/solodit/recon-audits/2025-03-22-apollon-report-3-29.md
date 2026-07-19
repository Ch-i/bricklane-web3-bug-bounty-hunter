---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-29
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-30] Donation on Pairs, in conjunction with lax slippage could be used to
  take on unintended ratios of debt'
vuln_class: []
---

# [L-30] Donation on Pairs, in conjunction with lax slippage could be used to take on unintended ratios of debt

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Executive Summary**

Pair.synch allows synching without a swap being performed

This is a donation to the Pair reserves, which changes it's price

**Impact**

When providing liquidity the ratio of the two tokens is taken into account

Via donation attacks we can force people to take on incorrect ratios of debt

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L228-L302

```solidity
  function addLiquidity(
    address tokenA,
    address tokenB,
    uint amountADesired,
    uint amountBDesired,
    uint amountAMin,
    uint amountBMin,
    PriceUpdateAndMintMeta memory _priceAndMintMeta,
    uint deadline
  ) public payable virtual override ensure(deadline) returns (uint amountA, uint amountB, uint liquidity) {
    ProvidingVars memory vars;
    vars.pair = getPair[tokenA][tokenB]; /// @audit QA not sorting tokens means this can revert | No fix is ok but it's a gotcha
    if (vars.pair == address(0)) revert PairDoesNotExist();
    /// @audit not checking that min < desired - S
    {
      (vars.reserveA, vars.reserveB) = getReserves(tokenA, tokenB);
      if (vars.reserveA == 0 && vars.reserveB == 0) {
        (amountA, amountB) = (amountADesired, amountBDesired); /// @audit First LP Can attack by massively imbalancing by performing a single sided swap or similar
      } else {
        uint amountBOptimal = quote(amountADesired, vars.reserveA, vars.reserveB);
        if (amountBOptimal <= amountBDesired) {
          if (amountBOptimal < amountBMin) revert InsufficientBAmount();
          (amountA, amountB) = (amountADesired, amountBOptimal);
        } else {
          uint amountAOptimal = quote(amountBDesired, vars.reserveB, vars.reserveA);
          assert(amountAOptimal <= amountADesired); /// @audit Looks wrong
          if (amountAOptimal < amountAMin) revert InsufficientAAmount();
          (amountA, amountB) = (amountAOptimal, amountBDesired);
        }
      }
    }
    // AmountA and B = Amts after optimal math

    vars.senderBalanceA = IERC20(tokenA).balanceOf(msg.sender);
    vars.senderBalanceB = IERC20(tokenB).balanceOf(msg.sender);
    // Pick Min between available and optimal
    vars.fromBalanceA = LiquityMath._min(vars.senderBalanceA, amountA); /// @audit WHY?
    vars.fromBalanceB = LiquityMath._min(vars.senderBalanceB, amountB);
    // Optimal - From Balance
    vars.fromMintA = amountA - vars.fromBalanceA;
    vars.fromMintB = amountB - vars.fromBalanceB;

    // mint new tokens if the sender did not have enough
    if (vars.fromMintA != 0 || vars.fromMintB != 0) {
      TokenAmount[] memory debtsToMint;
      if (vars.fromMintA != 0 && vars.fromMintB != 0) {
        // mint both
        debtsToMint = new TokenAmount[](2);
        debtsToMint[0] = TokenAmount(tokenA, vars.fromMintA);
        debtsToMint[1] = TokenAmount(tokenB, vars.fromMintB);
      } else {
        // mint only 1 token
        debtsToMint = new TokenAmount[](1);
        debtsToMint[0] = (
          vars.fromMintA != 0
            ? TokenAmount(tokenA, vars.fromMintA) // mint A
            : TokenAmount(tokenB, vars.fromMintB) // mint B
        );
      }
      borrowerOperations.increaseDebt{ value: msg.value }(
        msg.sender, // OK 
        vars.pair, // OK
        debtsToMint, // OK - See above
        _priceAndMintMeta.meta, /// @audit this looks griefable | TODO
        _priceAndMintMeta.priceUpdateData // TODO
      );
    }

    // transfer tokens sourced from senders balance
    if (vars.fromBalanceA != 0) safeTransferFrom(tokenA, msg.sender, vars.pair, vars.fromBalanceA);
    if (vars.fromBalanceB != 0) safeTransferFrom(tokenB, msg.sender, vars.pair, vars.fromBalanceB);

    // deposit into staking
    liquidity = ISwapPair(vars.pair).mint(msg.sender); /// @audit-ok this doesn't send tokens, it credits the stakingPool Deposit to msg.sender
  }
```

This can be abused to cause losses whenever the slippage checks are not set tight enough


**Mitigation**

Setting highly accurate slippage settings will prevent this
