---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: '`LibTokenSilo::calculateGrownStalkAndStem` appears to perform redundant calculations
  on the `grownStalk` parameter'
vuln_class: []
---

# `LibTokenSilo::calculateGrownStalkAndStem` appears to perform redundant calculations on the `grownStalk` parameter

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

[`LibTokenSilo::calculateGrownStalkAndStem`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L433-L441) is used in [`ConvertFacet::_depositTokensForConvert`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L209) when calculating the grown stalk to be minted and stem index at which the corresponding deposit is to be made, accounting for the current grown stalk and Bean Denominated Value (BDV). Assuming no rounding, it appears that the calculations performed on `grownStalk` are redundant:

$\text{stem} = \text{\_stemTipForToken} - \frac{\text{grownStalk}}{\text{bdv}}$

$\text{\_grownStalk} = (\text{\_stemTipForToken} - \text{stem}) \times \text{bdv}$

$= (\text{\_stemTipForToken} - (\text{\_stemTipForToken} - \frac{\text{grownStalk}}{\text{bdv}})) \times \text{bdv}$

$= \frac{\text{grownStalk}}{\text{bdv}} \times \text{bdv}$

$= \text{grownStalk}$

$\therefore \text{\_grownStalk} \equiv \text{grownStalk}$

It is therefore recommended to perform the following modification:

```diff
    // LibTokenSilo.sol
    function calculateGrownStalkAndStem(address token, uint256 grownStalk, uint256 bdv)
        internal
        view
        returns (uint256 _grownStalk, int96 stem)
    {
        int96 _stemTipForToken = stemTipForToken(token);
        stem = _stemTipForToken.sub(toInt96(grownStalk.div(bdv)));
-       _grownStalk = uint256(_stemTipForToken.sub(stem).mul(toInt96(bdv)));
+       _grownStalk = grownStalk;
    }
```
