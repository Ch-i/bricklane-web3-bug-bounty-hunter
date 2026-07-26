---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: '`LibLockedUnderlying` regression might not be representative of the expected
  behaviour'
vuln_class: []
---

# `LibLockedUnderlying` regression might not be representative of the expected behaviour

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

The percentage of locked liquidity, used in determining the L2SR in `LibEvaluate`, is obtained through the implementation of an on-chain look-up table based on an off-chain linear regression. The assumption considered acceptable for both Unripe Bean and Unripe LP is that 46,659 Unripe Tokens are chopped at each step. This number is calculated by dividing the number of Unripe Tokens by the number of Unripe Token Holders, resulting in an average of 46,659 Unripe Tokens held per Farmer with a non-zero balance. 2000 is used as a slight overestimation of the number of holders for both Unripe Bean and Unripe LP. An overestimation is acceptable because it results in a more conservative L2SR.

However, this average might not accurately represent what is expected in each Chop. For example, consider a scenario where 9 users each have 100,000 Unripe Tokens, and one user has 5.1 million Unripe Tokens.

$$\frac{Number\ of \ Unripe\; Tokens}{Number\ of \ Unripe\ Token \ Holders}= \frac{9 \times 100.000 + 5.100.000}{10} =$$

$$\frac{900.000 + 5.100.000}{10} = \frac{6.000.000}{10}=600.000$$

In this case, the regression would consider that `600,000` Unripe Tokens are Chopped in each step, which can actually be done by just one single user. Therefore, here it would be better to use the mode or median values rather than the mean.
