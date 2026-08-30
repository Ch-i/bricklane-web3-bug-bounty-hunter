---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-1-10
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Incorrect rounding of rate in favor of users when they buy DS Tokens
vuln_class: []
---

# Incorrect rounding of rate in favor of users when they buy DS Tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** Consider this line in `Helper::normalizeRate` which always rounds down:
```solidity
26:            return value / (10**(fromDecimals - toDecimals));
```

`Helper::normalizeRate` is called by `RedStoneNavProvider::rate`, which is called by both `SecuritizeOnRamp.sol` and `SecuritizeOffRamp.sol`.

`SecuritizeOnRamp::calculateDsTokenAmount` is used to buy DSTokens and does this:
```solidity
rate = navProvider.rate(); // assumed to be in `assetDecimals`

dsTokenAmount = (liquidityAmountExcludingFee * (10 ** (2 * assetDecimals))) / (rate * (10 ** liquidityTokenDecimals));
```

Since `rate` is used in the denominator, a smaller value due to rounding down results in the user getting slightly more DSTokens.

**Impact:** Incorrect rounding of rate in favor of users gives users slightly more DSTokens than they should receive.

**Recommended Mitigation:** * `ISecuritizeNavProvider::rate` should have an input parameter which specifies rounding direction so that callers can specify the appropriate rounding direction based on their needs
* the rounding direction should be passed as input to `Helper::normalizeRate`
* `Helper::normalizeRate` should use OZ [Math::mulDiv](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol#L282) with explicit rounding at L26 where it performs division

**Securitize:** Acknowledged for now as we don't want to change the interface at this time. In a real life scenario there shouldn't be any actual impact because for Redstone Push model they update the price querying our API, and our price never exceeds token decimals. So normally Redstone price has 8 decimals and our tokens 6, so it leads in a price with two zeros at the end.
