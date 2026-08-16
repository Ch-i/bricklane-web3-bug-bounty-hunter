---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Potentially unsafe cast from negative `int96` values
vuln_class: []
---

# Potentially unsafe cast from negative `int96` values

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** Where calculations are performed on `int96` values, for example when manipulating stems in [`LibSilo::stalkReward`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibSilo.sol#L634-L638), [`LibTokenSilo::grownStalkForDeposit`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L422), and [`LibTokenSilo::calculateGrownStalkAndStem`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L452), Beanstalk uses the `LibSafeMathSigned96` library. Based on the invariant that the stem for a new deposit should never exceed the stem tip for a given token, casting these values to `uint256` is fine since the difference between the two stem values should never be negative. However, in the event of a bug that violates this invariant, it could be possible to have a negative `int96` value cast to a very large `uint256` value, potentially resulting in a huge amount of stalk being minted.

This issue is already sufficiently [mitigated](https://github.com/BeanstalkFarms/Beanstalk/blob/08ca0d7d495c94f2a4366fb7f99da561b74cc1c0/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L419-L422) in `LibTokenSilo::grownStalkForDeposit` and it appears the instance in `LibTokenSilo::calculateGrownStalkAndStem` can never reach this state. Additional logic should similarly be added to `LibSilo::stalkReward` to ensure that the result of subtraction is positive and thus the cast to `uint256` is safe.

**Impact:** While it appears not currently exploitable, a bug in the calculation of the stem for a given deposit or stem tip for a given token in `LibSilo::stalkReward` could result in the erroneous minting of a large amount of stalk.

**Proof of Concept:** The following forge test demonstrates this issue:
```solidity
contract TestStemsUnsafeCasting is Test {
    using LibSafeMathSigned96 for int96;

    function stalkReward(int96 startStem, int96 endStem, uint128 bdv)
        internal
        view
        returns (uint256)
    {
        int96 reward = endStem.sub(startStem).mul(int96(bdv));
        console.logInt(reward);
        console.logUint(uint128(reward));

        return uint128(reward);
    }

    function test_stalk_reward() external {
        uint256 reward = stalkReward(1200, 1000, 1337);
        console.logUint(reward);
    }
}
```

**Recommended Mitigation:** Add additional logic to safely perform the cast from `int96` or otherwise handle the case where the result of stem subtraction could be negative.
