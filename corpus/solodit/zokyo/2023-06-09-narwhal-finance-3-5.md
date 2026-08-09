---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: No need for Safe Math costly computation
vuln_class: []
---

# No need for Safe Math costly computation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Description**

Vester.sol/VesterNLP.sol & VestingSchedule.sol - Methods: _mintPair, _burnPair, _mint, _burn, some arithmetic operations are checked unnecessarily as the conditions for it to pass without overflow/underflow is already existing.
```solidity
// _burnPair
pairAmounts[_account] = pairAmounts[_account].sub(_amount,"Vester: burn amount exceeds balance");
pairSupply = pairSupply.sub(_amount);

// _mintPair
pairSupply = pairSupply.add(_amount);
pairAmounts[_account] = pairAmounts[_account].add(_amount);

// _burn
balances[_account] = balances[_account].sub(_amount,"Vester: burn amount exceeds balance");
totalSupply = totalSupply.sub(_amount);

// _mint
totalSupply = totalSupply.add(_amount);
balances[_account] = balances[_account].add(_amount);

Given that balances <= totalSupply and pairAmounts <= pairSupply, In _mint() there is no need to safely add same amount to balances if the summation already passed the totalSupply addition without overflow, same in _mintPair(). In _burn() there is no need to safely subtract same amount from totalSupply if the subtraction already passed the balances subtraction, same in _burnPair().
Same applies to VestingSchedule
// _mint
totalSupply = totalSupply.add(_amount);
balances[_account] = balances[_account].add(_amount);

// _burn
balances[_account] = balances[_account].sub(_amount, "Vester: burn amount exceeds balance");
totalSupply = totalSupply.sub(_amount);
```

**Recommendation** 

Use unchecked block on these arithmetic operations to save the compute cost.

**Fix** -  As of  commit a72e06b , informational note is acknowledged and no change by dev team. There is no significance in this note as it does not affect the logic nor introduce a vulnerability.
