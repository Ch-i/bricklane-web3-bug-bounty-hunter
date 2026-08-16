---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-14-cyfrin-goldilocks-v1-1-1-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md
tags:
- firm:cyfrin
- report:2024-04-14-cyfrin-goldilocks-v1-1
title: In `Goldigovernor`, wrong assumption of block time
vuln_class: []
---

# In `Goldigovernor`, wrong assumption of block time

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-14-cyfrin-goldilocks-v1.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-14-cyfrin-goldilocks-v1.1.md)_

---

**Severity:** Medium

**Description:** In `Goldigovernor.sol`, voting period/delay limits are set with 15s block time.

```solidity
  /// @notice Minimum voting period
  uint32 public constant MIN_VOTING_PERIOD = 5760; // About 24 hours

  /// @notice Maximum voting period
  uint32 public constant MAX_VOTING_PERIOD = 80640; // About 2 weeks

  /// @notice Minimum voting delay
  uint32 public constant MIN_VOTING_DELAY = 1;

  /// @notice Maximum voting delay
  uint32 public constant MAX_VOTING_DELAY = 40320; // About 1 week
```

But Berachain has 5s block time according to [its documentation](https://docs.berachain.com/faq/#how-well-does-berachain-perform).

```
Berachain has the following properties:

- Block time: 5s
```

So these limits will be set shorter than expected.

**Impact:** Voting period/delay limits will be set shorter than expected.

**Recommended Mitigation:** We should calculate these limits with 5s block time.

**Client:** Fixed in [PR #14](https://github.com/0xgeeb/goldilocks-core/pull/14)

**Cyfrin:** Verified.
