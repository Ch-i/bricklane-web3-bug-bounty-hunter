---
affected_contracts: []
derives_from: []
id: solodit-0x52-2025-05-02-hyperstable-1-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
tags:
- firm:0x52
- report:2025-05-02-hyperstable
title: '[M-04] `AdaptiveIRM#_curve` multiples instead of dividing leading to "V" shaped
  curve instead of expected "L" shaped curve'
vuln_class: []
---

# [M-04] `AdaptiveIRM#_curve` multiples instead of dividing leading to "V" shaped curve instead of expected "L" shaped curve

_Section severity (from Solodit section header): Medium_  
_Audit firm: 0x52_  
_Source report: [2025-05-02-Hyperstable.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md)_

---

**Details**

[AdaptiveIRM.sol#L110-L115](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/libraries/AdaptiveIRM.sol#L110-L115)

        function _curve(int256 _rateAtTarget, int256 err) private pure returns (int256) {
            // Non negative because 1 - 1/C >= 0, C - 1 >= 0.
    @>      int256 coeff = err < 0 ? INT_WAD - INT_WAD.sMulWad(CURVE_STEEPNESS) : CURVE_STEEPNESS - INT_WAD;
            // Non negative if _rateAtTarget >= 0 because if err < 0, coeff <= 1.
            return (coeff.sMulWad(err) + INT_WAD).sMulWad(int256(_rateAtTarget));
        }

Above is the `_curve` calculation for the forked `adaptiveIrm`. Below is the original `adaptiveIRM` contract from `Morpho`.

[AdaptiveCurveIrm.sol#L136-L141](https://github.com/morpho-org/morpho-blue-irm/blob/0e99e647c9bd6d3207f450144b6053cf807fa8c4/src/adaptive-curve-irm/AdaptiveCurveIrm.sol#L136-L141)

        function _curve(int256 _rateAtTarget, int256 err) private pure returns (int256) {
            // Non negative because 1 - 1/C >= 0, C - 1 >= 0.
    @>      int256 coeff = err < 0 ? WAD - WAD.wDivToZero(ConstantsLib.CURVE_STEEPNESS) : ConstantsLib.CURVE_STEEPNESS - WAD;
            // Non negative if _rateAtTarget >= 0 because if err < 0, coeff <= 1.
            return (coeff.wMulToZero(err) + WAD).wMulToZero(int256(_rateAtTarget));
        }

Notice that the `WAD.wDivToZero` has been erroneously replaced with `INT_WAD.sMulWad`. err is the distance between the current utilization and the target utilization. As a result of this change the interest rate curve will decrease as it's approaching from the left rather than increasing as intended. This will give a "V" shaped interest rate curve rather than an "L" shaped one.

**Lines of Code**

[AdaptiveIRM.sol#L110-L115](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/libraries/AdaptiveIRM.sol#L110-L115)

**Recommendation**

Change the mul to a div

**Remediation**

Fixed in [6cc2ad9](https://github.com/hyperstable/contracts/commit/6cc2ad9f1289195ece0e7c2d4cd7e2dc58e771db) as recommended.
