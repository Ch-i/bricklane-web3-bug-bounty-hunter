---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-08] `BorrowerOperations` alters user debt but enforces prices are not stale
  only for debts that are being actively altered'
vuln_class: []
---

# [M-08] `BorrowerOperations` alters user debt but enforces prices are not stale only for debts that are being actively altered

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

A common pattern used in Apollon for price validation looks as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L248-L270

```solidity
  function addColl(
    TokenAmount[] memory _colls,
    address _upperHint,
    address _lowerHint,
    bytes[] memory _priceUpdateData
  ) public payable override {
    address borrower = msg.sender;
    (ContractsCache memory contractsCache, LocalVariables_adjustTrove memory vars) = _prepareTroveAdjustment(
      borrower,
      _priceUpdateData,
      false
    );

    // revert debt token deposit if prices are untrusted
    for (uint i = 0; i < _colls.length; i++) {
      if (!contractsCache.tokenManager.isDebtToken(_colls[i].tokenAddress)) continue;

      TokenPrice memory tokenPriceEntry = contractsCache.priceFeed.getTokenPrice(
        vars.priceCache,
        _colls[i].tokenAddress
      );
      if (!tokenPriceEntry.isPriceTrusted) revert UntrustedOraclesDebtTokenDeposit(); /// @audit verifying Colls
    } /// But this is user param not all colls the user has
```

Where `_cols` is a user provided parameter

Similarly to increase debt:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L372-L395

```solidity
  function _increaseDebt(
    address _borrower,
    address _to,
    TokenAmount[] memory _debts,
    MintMeta memory _meta,
    bytes[] memory _priceUpdateData
  ) internal {
    (ContractsCache memory contractsCache, LocalVariables_adjustTrove memory vars) = _prepareTroveAdjustment(
      _borrower,
      _priceUpdateData,
      true //will be called by swap operations, that handled the price update
    );

    _requireValidMaxFeePercentage(contractsCache.troveManager, _meta.maxFeePercentage, vars.isInRecoveryMode);
    for (uint i = 0; i < _debts.length; i++) {
      _requireNonZeroDebtChange(_debts[i].amount);

      // revert minting if the oracle is untrusted
      TokenPrice memory tokenPriceEntry = contractsCache.priceFeed.getTokenPrice(
        vars.priceCache,
        _debts[i].tokenAddress
      );
      if (!tokenPriceEntry.isPriceTrusted) revert UntrustedOraclesMintingIsFrozen();
    }
```

Where `debts` is passed by `SwapOperations`

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapOperations.sol#L271-L293

```solidity
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
```

This risks missing:
- Multiple other debts -> When a user takes on more than one stock debt token
- Multiple other collaterals -> When a user has already used other collaterals for it's Collateralization Ratio

Due to this, multiple possible oracle related exploits are possible such as:
- Over borrowing
- Self-liquidation by borrowing and then updating a price
- Bypassing the restrictions on triggering Recovery mode

*Instances*
- `addColl`
- `withdrawColl`
- `increaseDebt`

**Mitigation**

I believe all prices must be validated for staleness, offering the ability of chosing between the Pyth and the Alternative Feed should be viewed as a risky opening for arbitrage, self-liquidations and recovery mode liquidations
