---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Migration of unripe LP from BEAN:3CRV to BEAN:ETH does not account for recapitalization
  accounting error
vuln_class: []
---

# Migration of unripe LP from BEAN:3CRV to BEAN:ETH does not account for recapitalization accounting error

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

**Description:** The global [`AppStorage::recapitalized`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/AppStorage.sol#L485) state refers to the dollar amount recapitalized when Fertilizer was bought with USDC and paired with BEAN for BEAN:3CRV LP. When removing this underlying liquidity and swapping 3CRV for WETH during the migration of unripe LP, it is very likely that the BCM will experience some slippage. This is more likely to be the case if the swap is made on the open market rather than an OTC deal, but either way it is likely that the dollar value of the resulting WETH, and hence BEAN:ETH LP, will be less than it was as BEAN:3CRV before the migration. Currently, [`UnripeFacet::addMigratedUnderlying`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L257) updates the BEAN:ETH LP token balance underlying the unripe LP, completing the migration, but does not account for any changes in the dollar value as outlined above. Based on the current implementation, it is very likely that the BCM will complete migration by transferring less in dollar value while the recapitalization status remains the same, causing inconsistency in [`LibUnripe::percentLPRecapped`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/LibUnripe.sol#L30-L36) and `LibUnripe::add/removeUnderlying` which are used in the conversion of urBEAN ↔ urBEANETH in `LibUnripeConvert`. Therefore, the global recapitalized state should be updated to reflect the true dollar value of recapitalization on completion of the migration.

**Impact:** Once sufficiently funded by purchasers of Fertilizer, it is possible that recapitalization could be considered completed with insufficient underlying BEAN:ETH LP. This amounts to a loss of user funds since the true recapitalized amount will be less than that specified by [`C::dollarPerUnripeLP`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/C.sol#L190-L192) which is used to calculate the total dollar liability in [`LibFertilizer::remainingRecapitalization`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/LibFertilizer.sol#L159-L163).

**Recommended Mitigation:** Reassign `s.recapitalized` to the oracle USD amount of the new BEAN:ETH LP at the time of migration completion.

```diff
    function addMigratedUnderlying(address unripeToken, uint256 amount) external payable nonReentrant {
        LibDiamond.enforceIsContractOwner();
        IERC20(s.u[unripeToken].underlyingToken).safeTransferFrom(
            msg.sender,
            address(this),
            amount
        );
        LibUnripe.incrementUnderlying(unripeToken, amount);

+       uint256 recapitalized = amount.mul(LibEthUsdOracle.getEthUsdPrice()).div(1e18);
+       require(recapitalized != 0, "UnripeFacet: cannot calculate recapitalized");
+       s.recapitalized = s.recapitalized.add(recapitalized);
    }
```

**Beanstalk Farms:** This is intentional – the cost of slippage goes to the Unripe LP token holders. This should be clearly stated in the BIP draft.

**Cyfrin:** Acknowledged.
