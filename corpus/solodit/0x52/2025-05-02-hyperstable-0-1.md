---
affected_contracts: []
derives_from: []
id: solodit-0x52-2025-05-02-hyperstable-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-02T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md
tags:
- firm:0x52
- report:2025-05-02-hyperstable
title: '[H-02] `EmissionScheduler#epochEmission` lacks access control and can be called
  by anyone to cause epoch to mint no emissions'
vuln_class: []
---

# [H-02] `EmissionScheduler#epochEmission` lacks access control and can be called by anyone to cause epoch to mint no emissions

_Section severity (from Solodit section header): High_  
_Audit firm: 0x52_  
_Source report: [2025-05-02-Hyperstable.md](https://github.com/solodit/solodit_content/blob/main/reports/0x52/2025-05-02-Hyperstable.md)_

---

**Details**

[EmissionScheduler.sol#L63-L80](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L63-L80)

    @>  function epochEmission(uint256 _pegSupply, uint256 _veSupply) external returns (uint256, uint256, uint256) {
            uint256 currentEpoch = _currentEpoch();

            if (currentEpoch == lastEpoch) {
                return (0, 0, 0);
            }

    @>      lastEpoch = currentEpoch;

            uint256 toEmit = (_pegSupply - _veSupply).mulDiv(2, EMISSION_PRECISION);

            lastEpochEmission = toEmit;

            uint256 rebase = _calculateRebase(toEmit, _pegSupply, _veSupply);
            uint256 teamEmission = _calculateTeamEmission(toEmit, rebase);

            return (toEmit, rebase, teamEmission);
        }

We see above that `lastEpoch` is updated to `currentEpoch` when called. Also notice that there is no access control on calls to this function and therefore it can be called by anyone. The result in that when the legitimate call is made it will return `(0, 0, 0)`, completely wipe out all emissions owed for the epoch.

**Lines of Code**

[EmissionScheduler.sol#L63-L80](https://github.com/hyperstable/contracts/blob/35db5f2d3c8c1adac30758357fbbcfe55f0144a3/src/governance/EmissionScheduler.sol#L63-L80)

**Recommendation**

`epochEmission` should only be callable by `minter`.

**Remediation**

Fixed in [7866674](https://github.com/hyperstable/contracts/commit/786667407e84ff76111aa0a8213b698f791f532d). Creates `_onlyMinter` which provides access control and applies it to `EmissionScheduler#epochEmission`.
