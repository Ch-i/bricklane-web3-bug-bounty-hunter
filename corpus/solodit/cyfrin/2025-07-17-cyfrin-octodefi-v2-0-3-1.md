---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Positive Pyth oracle exponents should be explicitly handled
vuln_class: []
---

# Positive Pyth oracle exponents should be explicitly handled

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `PriceOracle._scalePythPrice()` assumes that the exponent `_expo` will always be negative:

```solidity
    function _scalePythPrice(int256 _price, int32 _expo) internal pure returns (uint256) {
        if (_price < 0) {
            revert NegativePriceNotAllowed();
        }

@>      uint256 _absExpo = uint32(-_expo);

        if (_expo <= -18) {
            return uint256(_price) * (10 ** (_absExpo - 18));
        }

        return uint256(_price) * 10 ** (18 - _absExpo);
    }
```

While this assumption is [not likely to be violated](https://x.com/abarbatei/status/1901327645373030711), it is possible for the exponent to be configured as a positive value based on its signed type and usage in [other libraries](https://github.com/pyth-network/pyth-crosschain/blob/main/target_chains/ethereum/sdk/solidity/PythUtils.sol).

If the protocol were to ever rely on a Pyth oracle with a positive exponent then `uint32(-expo)` could silently underflow, resulting in a huge absolute value and causing execution to revert during the final scaling.

**Recommended Mitigation:** Consider explicitly handling the case where the exponent is positive.

**OctoDeFi:** Fixed in PR [\#19](https://github.com/octodefi/strategy-builder-plugin/pull/19).

**Cyfrin:** Verified. The positive exponent case is now explicitly handled.
