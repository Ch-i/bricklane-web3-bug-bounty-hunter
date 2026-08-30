---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Incorrect handling of decimals in `LibLockedUnderlying::getPercentLockedUnderlying`
  results in an incorrect value being returned, affecting the temperature and Bean
  to maxLP gaugePoint per BDV ratio updates in each subsequent call to `Seaso
vuln_class: []
---

# Incorrect handling of decimals in `LibLockedUnderlying::getPercentLockedUnderlying` results in an incorrect value being returned, affecting the temperature and Bean to maxLP gaugePoint per BDV ratio updates in each subsequent call to `SeasonFacet::gm` when `unripe asset supply < 10M`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** Due to the Barn Raise and the associated Beans underlying Unripe assets, the number of tradable Beans does not equal the total Bean supply. Within the calculation of L2SR, the term "locked liquidity" refers to the portion of liquidity in the BEAN:ETH WELL that cannot be retrieved through chopping until the corresponding Fertilizer is paid.

The exchange ratio for the corresponding underlying asset can be summarized in the following formula:

$$\frac{Paid Fertilizer}{Minted Fertilizer} \times \frac{totalUnderlying(urAsset)}{supply(urAsset)}$$

The second factor indicates the amount of the underlying asset backing each unripe asset, while the first indicates the distribution of the underlying asset based on the ratio of Fertilizer that is already paid.

When a user chops an unripe asset, it is burned in exchange for a penalized amount of the underlying asset. The remaining underlying asset is now shared among the remaining unripe asset holders, meaning that if another user tries to chop the same amount of unripe asset at a given recapitalization rate, they will receive a greater amount of underlying asset.

For instance, assume that:
* 50% of the minted Fertilizer is paid
* A current supply of 70M
* An underlying amount of 22M

If Alice chops 1M unripe tokens:
$$1,000,000 \times 0.50 \times \frac{22,000,000}{70,000,000} =$$
$$1,000,000 \times 0.50 \times 0.31428 =$$
$$1,000,000 \times 0.50 \times 0.31428 =$$
$$1,000,000 \times 0.15714285 = $$
$$157,142.85$$

If Bob then chops the same amount of tokens:
$$1,000,000 \times 0.50 \times \frac{22,000,000-157,142.85}{70,000,000 - 1,000,000} =$$
$$1,000,000 \times 0.50 \times \frac{21,842,857.15}{69,000,000} =$$
$$1,000,000 \times 0.50 \times \frac{21,842,857.15}{69,000,000} =$$
$$1,000,000 \times 0.50 \times 0.3165 =$$
$$158,281.57$$

Given that the assumption of chopping the total unripe asset supply in one step is highly unlikely, the Beanstalk Farms team decided to perform an off-chain regression based on the average unripe asset per unripe asset holder. This yields an approximation for the percentage locked underlying token per asset based on the current unripe asset supply. An on-chain look-up table is used to retrieve the values of this regression; however, the issue with its implementation lies in its failure to account for unripe token decimals when compared with the inline conditional supply constants [`1_000_000`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L61), [`5_000_000`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L62), and [`10_000_000`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L63) as the intervals on which the iterative simulation was performed. Given these constants are not a fixed-point representation of the numbers they are intended to represent, [comparison](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L286) with the [6-decimal supply](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L60) will be incorrect.

**Impact:** Given that unripe assets have 6 decimals, `LibLockedUnderlying::getPercentLockedUnderlying` will tend to execute [this conditional branch](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibLockedUnderlying.sol#L63-L173), producing an incorrect calculation of locked underlying whenever the supply of the unripe asset is below 10M.

In the given scenario, this error would cascade into an incorrect calculation of L2SR, affecting how the temperature and Bean to maxLP gaugePoint per BDV ratio should be updated in the call to [`Weather::calcCaseIdandUpdate`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/sun/SeasonFacet/Weather.sol#L68) within [`SeasonFacet::gm`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L51).

**Proof of Concept:** A differential test (see Appendix A) was written to demonstrate this issue based on CSV provided by the Beanstalk Farms team. Modifications to the CSV include:
* Adding headers: recapPercentage, urSupply, lockedPercentage
* Generate a CSV without whitespaces
* Round the first column to 3 decimals
* For the third column, delete `e18` and round values to 18 decimals

**Recommended Mitigation:** Scale each inline constant that is compared against the unripe supply by 6 decimals.

For similar cases in the future, differential testing between the expected and actual outputs is effective in catching bugs of this type which rely on pre-computed off-chain values.
