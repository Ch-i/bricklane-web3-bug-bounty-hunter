---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-4-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Nesting `if`-statements is cheaper than using `andand`.
vuln_class: []
---

# Nesting `if`-statements is cheaper than using `andand`.

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

Nesting `if`-statements avoids the stack operations of setting up and using an extra jumpdest, and saves 6 gas.

```solidity
File: GovLocks.sol
214:     if (srcRep != dstRep && amt > 0) {
237:     if (nCheckpoints > 0 && checkpoints[delegatee][nCheckpoints - 1].fromBlock == block.number) {
266:     if(from != address(0) && to != address(0)) {

File: Goldilend.sol
536:     return _poolSize > 0 && supply > 0 ? FixedPointMathLib.mulWad(lockAmount, _GiBGTRatio(supply, _poolSize)) : lockAmount;

File: Goldiswap.sol
329:     if (elapsedIncrease >= 1 days && elapsedDecrease >= 1 days) {
```
