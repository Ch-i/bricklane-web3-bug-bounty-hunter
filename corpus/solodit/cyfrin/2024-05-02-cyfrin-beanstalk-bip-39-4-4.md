---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Cache updated remaining amount to prevent extra storage read
vuln_class: []
---

# Cache updated remaining amount to prevent extra storage read

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`FundraiserFacet::fund` should save the calculated [`remaining - amount`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/field/FundraiserFacet.sol#L124) then use it to set storage in [L125](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/field/FundraiserFacet.sol#L125) and to check for completion in [L128](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/field/FundraiserFacet.sol#L128); this prevents re-reading storage again in L128. One easy solution is to reuse the existing `remaining` stack variable:

```solidity
remaining = remaining - amount; // Note: SafeMath is redundant here.
s.fundraisers[id].remaining = remaining;
emit FundFundraiser(msg.sender, id, amount);

// If completed, transfer tokens to payee and emit an event
if (remaining == 0) {
    _completeFundraiser(id);
}
```

Consider this simplified example using Foundry:
```solidity
uint256 private s_remainingDebt = 10;

function _onDebtRepayment() private {}

function testRemaining1() public {
    uint256 repaymentAmount = 10;

    // update storage
    s_remainingDebt -= repaymentAmount;

    // use storage read for check
    if(s_remainingDebt == 0) {
        _onDebtRepayment();
    }

    assert(s_remainingDebt == 0);
}

function testRemaining2() public {
    uint256 repaymentAmount = 10;

    // cache remaining debt
    uint256 remainingDebt = s_remainingDebt - repaymentAmount;
    // update storage
    s_remainingDebt = remainingDebt;

    // use cache for check
    if(remainingDebt == 0) {
        _onDebtRepayment();
    }

    assert(s_remainingDebt == 0);
}

[PASS] testRemaining1() (gas: 621)
[PASS] testRemaining2() (gas: 563)
```
