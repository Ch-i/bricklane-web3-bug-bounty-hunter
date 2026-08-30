---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Missing validation in `LibWhitelist::verifyTokenInLibWhitelistedTokens`
vuln_class: []
---

# Missing validation in `LibWhitelist::verifyTokenInLibWhitelistedTokens`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** Prior to the introduction of [`LibWhitelistedToken.sol`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibWhitelistedTokens.sol), Beanstalk did not have a way of iterating through its whitelisted tokens. To mitigate against an upgrade where a new asset is whitelisted, but `LibWhitelistedToken.sol` is not updated, [`LibWhitelist::verifyTokenInLibWhitelistedTokens`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Silo/LibWhitelist.sol#L196-L217) verifies that the token is both in the correct array(s) and not in invalid arrays.

While `LibWhitelistedTokens::getWhitelistedWellLpTokens` is supposed to return a subset of whitelisted LP tokens, this is not guaranteed. In this case, if the token is either Bean or an Unripe Token, the first `else` block within `LibWhitelist::verifyTokenInLibWhitelistedTokens` should also check that the token is not in the whitelisted Well LP token array.

**Recommended Mitigation:**
```diff
} else {
    checkTokenNotInArray(token, LibWhitelistedTokens.getWhitelistedLpTokens());
+   checkTokenNotInArray(token, LibWhitelistedTokens.getWhitelistedWellLpTokens());
}
```
