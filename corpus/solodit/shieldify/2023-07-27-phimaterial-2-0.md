---
affected_contracts: []
derives_from: []
id: solodit-shieldify-2023-07-27-phimaterial-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-07-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
tags:
- firm:shieldify
- report:2023-07-27-phimaterial
title: '[L-01] Usage of `ecrecover` Should Be Replaced with Usage of OpenZeppelin''s
  `ECDSA` Library'
vuln_class: []
---

# [L-01] Usage of `ecrecover` Should Be Replaced with Usage of OpenZeppelin's `ECDSA` Library

_Section severity (from Solodit section header): Low_  
_Audit firm: Shieldify_  
_Source report: [2023-07-27-PHIMaterial.md](https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md)_

---

**Severity**

Low Risk

**Description**

[Signature malleability](https://swcregistry.io/docs/SWC-117) is one of the potential issues with `ecrecover`. The `_isVerifiedCoupon` function calls the Solidity `ecrecover()` function directly to verify the given signatures. However, the `ecrecover()` retrieves the address of the signer via a provided `v`, `r` and `s` signatures. However, due to the nature of the elliptic curve digital signing algorithm (ECDSA), there are two valid points (i.e. two `s` values) on the elliptic curve with the exact same `r` value. An attacker can pretty easily compute the other valid `s` value on the elliptic curve that will return the same original signer, making the signature malleable.

`ecrecover()` allows malleable (non-unique) signatures and thus is susceptible to replay attacks. This means that multiple signatures will be considered valid, which will lead to wrong claim logic.

**Location of Affected Code**

File: [`src/PhiDaily.sol#L161`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/PhiDaily.sol#L161)

```solidity
address signer = ecrecover(digest, coupon.v, coupon.r, coupon.s);
```

**Recommendation**

Use the `recover()` function from OpenZeppelin's ECDSA library to verify the uniqueness of the signature. Using this library implements a check on the value of the `s` variable to ensure that only one of its possible inputs is valid. Ensure that you are using a version `> 4.7.3` for there was a critical bug `>= 4.1.0` `< 4.7.3`.

**Team Response**

Acknowledged and fixed by using `ECDSA` library.
