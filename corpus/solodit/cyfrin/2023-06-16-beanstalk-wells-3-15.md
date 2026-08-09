---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-15
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Precision loss on large values transformed between log2 scale and the normal
  scale
vuln_class: []
---

# Precision loss on large values transformed between log2 scale and the normal scale

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

In `GeoEmaAndCumSmaPump.sol::_init`, the reserve values are transformed into log2 scale:

```solidity
byteReserves[i] = reserves[i].fromUIntToLog2();
```

This transformation implies a precision loss, particularly for large `uint256` values, as demonstrated by the following test:

```solidity
function testUIntMaxToLog2() public {
uint x = type(uint).max;
bytes16 y = ABDKMathQuad.fromUIntToLog2(x);
console.log(x);
console.logBytes16(y);
assertEq(ABDKMathQuad.fromUInt(x).log_2(), ABDKMathQuad.fromUIntToLog2(x));
uint x_recover = ABDKMathQuad.pow_2ToUInt(y);
console.log(ABDKMathQuad.toUInt(y));
console.log(x_recover);
}
```

Consider explicit limiting of the reserve values to avoid precision loss.

**Beanstalk:** This is expected. Compressing a uint256 into a bytes16 can't possibly not lose precision as it is compressing 256 bits into 128 bits. E.g. there is only 113-bit decimal precision on the log operation. See [here](https://github.com/abdk-consulting/abdk-libraries-solidity/blob/master/ABDKMathQuad.md#ieee-754-quadruple-precision-floating-point-numbers).

**Cyfrin:** Acknowledged.
