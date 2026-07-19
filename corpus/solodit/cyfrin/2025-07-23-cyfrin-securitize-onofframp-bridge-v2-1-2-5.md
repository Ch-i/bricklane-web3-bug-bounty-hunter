---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Use of `msg.sender` instead of `_msgSender()` prevents meta-transaction support
vuln_class: []
---

# Use of `msg.sender` instead of `_msgSender()` prevents meta-transaction support

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** Several contracts in the codebase use `msg.sender` directly instead of `_msgSender()`, which prevents proper meta-transaction support. This inconsistency affects both initialization and core functionality across the system.

The affected contracts and functions include:

- `BaseContract::__BaseContract_init()`
- `SecuritizeOffRamp::redeem()`
- `SecuritizeBridge::bridgeDSTokens()`
- `SecuritizeBridge::validateLockedTokens()`

The protocol properly uses `_msgSender()` in their other functions and access control patterns, indicating awareness of meta-transaction support, but this was not consistently applied across all functions.

When a user performs a meta-transaction through a trusted forwarder:
1. The forwarder calls the contract on behalf of the user
2. Functions using `msg.sender` receive the forwarder's address instead of the user's address
3. Validation, authorization, and business logic fail or operate incorrectly

**Impact:** Meta-transaction functionality is broken as the forwarder contract becomes the transaction sender instead of the intended user, potentially causing authorization failures, incorrect event emissions, and improper validation logic.

**Recommended Mitigation:** Replace all instances of `msg.sender` with `_msgSender()` to support meta-transactions:

```diff
// BaseContract.sol
function __BaseContract_init() internal onlyInitializing {
    __UUPSUpgradeable_init();
    __Pausable_init();
-   __Ownable_init(msg.sender);
+   __Ownable_init(_msgSender());
}

// SecuritizeOffRamp.sol
function redeem(uint256 assetAmount, uint256 minOutputAmount) external whenNotPaused nonZeroNavRate nonZeroLiquidityProvider {
    uint256 rate = navProvider.rate();

-   RedemptionValidator.validateRedemption(msg.sender, assetAmount, asset);
+   RedemptionValidator.validateRedemption(_msgSender(), assetAmount, asset);

-   CountryValidator.validateCountryRestriction(msg.sender, dsServiceConsumer, restrictedCountries);
+   CountryValidator.validateCountryRestriction(_msgSender(), dsServiceConsumer, restrictedCountries);

    // ... calculations ...

    RedemptionManager.RedemptionParams memory params = RedemptionManager.RedemptionParams({
        asset: asset,
        liquidityProvider: liquidityProvider,
        feeManager: feeManager,
        assetAmount: assetAmount,
        liquidityTokenAmount: liquidityTokenAmount,
        minOutputAmount: minOutputAmount,
-       redeemer: msg.sender,
+       redeemer: _msgSender(),
        assetBurn: assetBurn
    });

    // ... execution logic ...

    emit RedemptionCompleted(
-       msg.sender,
+       _msgSender(),
        assetAmount,
        liquidityTokenAmount,
        rate,
        fee,
        address(liquidityProvider.liquidityToken())
    );
}

// SecuritizeBridge.sol
function bridgeDSTokens(uint16 targetChain, uint256 value) external override payable whenNotPaused {
    uint256 cost = quoteBridge(targetChain);
    require(msg.value >= cost, "Transaction value should be equal or greater than quoteBridge response");
-   require(dsToken.balanceOf(msg.sender) >= value, "Not enough balance in source chain to bridge");
+   require(dsToken.balanceOf(_msgSender()) >= value, "Not enough balance in source chain to bridge");

    // ... validation logic ...

-   require(registryService.isWallet(msg.sender), "Investor not registered");
+   require(registryService.isWallet(_msgSender()), "Investor not registered");

-   string memory investorId = registryService.getInvestor(msg.sender);
+   string memory investorId = registryService.getInvestor(_msgSender());

    // ... other logic ...

-   dsToken.burn(msg.sender, value, BRIDGE_REASON);
+   dsToken.burn(_msgSender(), value, BRIDGE_REASON);

    wormholeRelayer.sendPayloadToEvm{value: msg.value}(
        targetChain,
        targetAddress,
        abi.encode(
            investorDetail.investorId,
            value,
-           msg.sender,
+           _msgSender(),
            investorDetail.country,
            investorDetail.attributeValues,
            investorDetail.attributeExpirations
        ),
        0,
        gasLimit,
        whChainId,
-       msg.sender
+       _msgSender()
    );

-   emit DSTokenBridgeSend(targetChain, address(dsToken), msg.sender, value);
+   emit DSTokenBridgeSend(targetChain, address(dsToken), _msgSender(), value);
}

function validateLockedTokens(string memory investorId, uint256 value, IDSRegistryService registryService) private view {
    // ... compliance service logic ...

-   uint256 availableBalanceForTransfer = complianceService.getComplianceTransferableTokens(msg.sender, block.timestamp, uint64(lockPeriod));
+   uint256 availableBalanceForTransfer = complianceService.getComplianceTransferableTokens(_msgSender(), block.timestamp, uint64(lockPeriod));
    require(availableBalanceForTransfer >= value, "Not enough unlocked balance in source chain to bridge");
}
```

**Securitize:** Fixed in commit [045925](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/045925798158710fef70ecdd0e47da1974b37bfd) and commit [1da35c](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/1da35cde31a53e7b2de56de0d313ebdcb80cbfa3).

**Cyfrin:** Verified.
