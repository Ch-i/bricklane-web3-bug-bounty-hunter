---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: '`SiloFacet::transferDeposits` should only call `LibSiloPermit::_spendDepositAllowance`
  once'
vuln_class: []
---

# `SiloFacet::transferDeposits` should only call `LibSiloPermit::_spendDepositAllowance` once

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`SiloFacet::transferDeposits` currently loops through the input `amounts` array and [calls](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/silo/SiloFacet/SiloFacet.sol#L185) `LibSiloPermit::_spendDepositAllowance` once for each `amounts[i]`.

Instead, consider having a `totalAmount` stack variable that is incremented for each `amounts[i]` when looping through the inputs. Then, after the initial loop is complete, call `LibSiloPermit::_spendDepositAllowance` with `totalAmount` to save a significant number of storage reads & writes.

Consider this simplified example using Foundry:
```solidity
uint256 s_allowance = 10;

function _spendAllowance(uint256 amount) private {s_allowance-=amount;}

function testBulkTransfer1() public {
    // prepare input
    uint256[10] memory amounts;
    for(uint256 i=0; i<10; i++){amounts[i] = 1;}

    // function implementation; update storage 1-by-1
    for (uint256 i = 0; i < amounts.length; ++i) {
        _spendAllowance(amounts[i]);
    }

    assert(s_allowance == 0);
}

function testBulkTransfer2() public {
    // prepare input
    uint256[10] memory amounts;
    for(uint256 i=0; i<10; i++){amounts[i] = 1;}

    // function implementation; cache total amount, update storage once
    uint256 totalSpend;
    for (uint256 i = 0; i < amounts.length; ++i) {
        totalSpend += amounts[i];
    }

    _spendAllowance(totalSpend);

    assert(s_allowance == 0);
}

[PASS] testBulkTransfer1() (gas: 5494)
[PASS] testBulkTransfer2() (gas: 3435)
```
