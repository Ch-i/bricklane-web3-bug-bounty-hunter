---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-28
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-29] `SwapPair` is intended to overflow, but is not using `unchecked`'
vuln_class: []
---

# [L-29] `SwapPair` is intended to overflow, but is not using `unchecked`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Overflow logic from UniV2 no longer applies**

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L84-L93

```solidity
  function _update(uint balance0, uint balance1, uint112 _reserve0, uint112 _reserve1) private {
    if (balance0 > type(uint112).max || balance1 > type(uint112).max) revert Overflow();

    uint32 blockTimestamp = uint32(block.timestamp % 2 ** 32);
    uint32 timeElapsed = blockTimestamp - blockTimestampLast; // overflow is desired
    if (timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0) {
      // * never overflows, and + overflow is desired | /// @audit Overflow is wrong, this is solidity 0.8!!
      price0CumulativeLast += uint(UQ112x112.encode(_reserve1).uqdiv(_reserve0)) * timeElapsed;
      price1CumulativeLast += uint(UQ112x112.encode(_reserve0).uqdiv(_reserve1)) * timeElapsed;
    }
```

The code asserts that `+= overflow is desired` but this cannot happen on the current solidity version
This means that after (I think) more than a billion of volume, the pair can stop working

I can crunch the math, but the overflow is extremely unlikely

See: Velodrome (Which also ignores the overflow):
https://github.com/velodrome-finance/contracts/blob/9e5a5748c3e2bcef7016cc4194ce9758f880153f/contracts/Pool.sol#L212-L230

**Reserve overflow checks using `uint112` effectively cap any token max total supply**

The maximum amount possible is 2^122 - 1 

Which is basically `5.1922969e+15 * 1e18`

This should be sufficient, but it's worth keeping it in mind as you do not want to cross this value as it will break all pool operations for a pair

**Overflow exactly at time 2^32**

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/SwapPair.sol#L87-L88

```solidity
    uint32 blockTimestamp = uint32(block.timestamp % 2 ** 32);

```

This line being unchecked means the code will stop working at the timestamp 2^32

Which should be around Sun Feb 07 2106 06:28:16 GMT+0000

```solidity
    // forge test --match-test test_theOverflow -vv
    function test_theOverflow() public {
        vm.warp(type(uint32).max + 1);
        uint32 blockTimestamp = uint32(block.timestamp % 2 ** 32);

    }
```
