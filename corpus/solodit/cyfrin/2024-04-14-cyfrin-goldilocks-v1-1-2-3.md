---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: Inconsistent comparison while checking `eta`
vuln_class: []
---

# Inconsistent comparison while checking `eta`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Description:** In `Goldigovernor` and `Timelock`, inconsistent comparisons are used.

```solidity
File: Goldigovernor.sol
386:     else if (block.timestamp >= proposal.eta + Timelock(timelock).GRACE_PERIOD()) {
387:       return ProposalState.Expired;
388:     }

File: Timelock.sol
138:     if(block.timestamp > eta + GRACE_PERIOD) revert TxStale();
```
**Client:** Fixed in [PR #6](https://github.com/0xgeeb/goldilocks-core/pull/6)

**Cyfrin:** Verified.
