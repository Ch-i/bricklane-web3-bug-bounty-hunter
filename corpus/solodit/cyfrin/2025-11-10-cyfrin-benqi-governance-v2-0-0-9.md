---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-0-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: '`DistributionManagerSetup::canDistribute` should return false rather than
  reverting'
vuln_class: []
---

# `DistributionManagerSetup::canDistribute` should return false rather than reverting

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `DistributionManagerSetup::canDistribute` currently returns true if distribution can proceed but reverts from within `_validateCanDistribute()` if it cannot:

```solidity
    function canDistribute() public view returns (bool) {
        IClock clock = IClock(gaugeVoter.clock());
@>      _validateCanDistribute(clock);
        return true;
    }

    function _validateCanDistribute(IClock _clock) internal view {
@>      if (_activeRewardControllers.length() == 0) revert NoModulesConfigured();
@>      if (_clock.votingActive()) revert VotingStillActive();

        uint256 currentEpochId = _clock.currentEpoch();
        if (_isEpochDistributed(currentEpochId)) {
@>          revert EpochAlreadyDistributed(currentEpochId);
        }
    }
```

Rather than reverting, this view function should return false so it can be reliably called by consumers.

**BENQI:** Fixed in PR [\#20](https://github.com/aragon/benqi-governance/pull/20).

**Cyfrin:** Verified. A call to this function now either reverts or succeeds with empty return data.
