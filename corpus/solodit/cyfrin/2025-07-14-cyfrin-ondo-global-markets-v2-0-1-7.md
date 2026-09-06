---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-14-cyfrin-ondo-global-markets-v2-0-1-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-14-cyfrin-ondo-global-markets-v2-0
title: Test enhancements
vuln_class: []
---

# Test enhancements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-14-cyfrin-ondo-global-markets-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md)_

---

**Description:** * `GMIntegrationTest_GM_ETH`: Both tests [`test_hitRateLimits_onUSDInGMFlow_Subscribe`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/GM_IntegrationTest.t.sol#L1209-L1210) and [`test_hitRateLimits_onUSDInGMFlow_Redeem`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/GM_IntegrationTest.t.sol#L1254-L1255) have empty `expectReverts`:
   ```solidity
   // Should fail due to onUSD rate limit
   vm.expectRevert();
   gmTokenManager.mintWithAttestation(
     quote,
     signature,
     address(USDC),
     usdcAmount
   );
   ```
   Accepting any revert could hide unexpected errors allowing bugs to still pass the tests. Consider catching the expected revert:
   ```diff
       // Should fail due to onUSD rate limit
   -   vm.expectRevert();
   +   vm.expectRevert(OndoRateLimiter.RateLimitExceeded.selector);
       gmTokenManager.mintWithAttestation(
         quote,
         signature,
         address(USDC),
         usdcAmount
       );
   ```

* `GmTokenManagerSanityCheckOracleTest`: The test [`testPostPricesWithInvalidInput`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/tokenManager/GmTokenManagerSanityCheckOracleTest.t.sol#L563-L577) also has an empty `expectRevert()`. This test should ideally be split into two, `...WithInvalidToken`, `...WithInvalidPrice` and expect the correct errors: `InvalidAddress` and `PriceNotSet`.

* `error TokenPauseManagerClientUpgradeable.TokenPauseManagerCantBeZero` lacks a test. Consider adding one for assigning an invalid `TokenPauseManager`.

* `GMTokenManagerTest_ETH`: The test [`testMintFromNonKYCdSender`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/tokenManager/GmTokenManagerTest.t.sol#L587-L629) mentions a "KYC role" which doesn't exist. It also catches an empty revert on [L626](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/tokenManager/GmTokenManagerTest.t.sol#L626). This catch does not catch the correct error, it catches a `OneRateLimiter.RateLimitExceeded` error since the user has no rate limit config. Since the user is added to the registry on [L601](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/forge-tests/globalMarkets/tokenManager/GmTokenManagerTest.t.sol#L601), effectively saying it's KYC'd. Thus it passes the KYC check. Consider removing mentions of a KYC role, catching the correct revert (`IGMTokenManagerErrors.UserNotRegistered`) and remove the addition of the user to the registry.

**Cyfrin:** Fixed by Cyfrin in commit [`d3155d0`](https://github.com/ondoprotocol/rwa-internal/pull/469/commits/d3155d09d8bb0ed48b7975d758830fc60c36e525)
