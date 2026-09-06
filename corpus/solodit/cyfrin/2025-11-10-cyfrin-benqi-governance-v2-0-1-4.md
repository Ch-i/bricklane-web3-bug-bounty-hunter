---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Speed calculation precision handling is ineffective
vuln_class: []
---

# Speed calculation precision handling is ineffective

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** `SpeedCalculator::calcSpeed` intends to address precision loss by the application of the `SPEED_PRECISION` constant; however, its presence on both the numerator and denominator does nothing for precision loss as this factor is immediately divided back out:

```solidity
function calcSpeed(
    uint256 _votes,
    uint256 _totalVotes,
    uint256 _moduleBudget,
    uint256 _epochDuration
) public pure returns (uint256) {
    if (_totalVotes == 0 || _epochDuration == 0 || _votes == 0) return 0;

    return
        (_moduleBudget * SPEED_PRECISION * _votes) /
        (_epochDuration * _totalVotes * SPEED_PRECISION);
}
```

It would be better to reverse this scaling when calculating the market budget used, i.e. first performing the speed by duration multiplication. Only then should the result be divided back down, being careful to ensure that all other usage is equivalent as it is currently, e.g. when comparing with `MIN_SPEED` and current speeds on the comptroller/multi-distributor, given that this logic is implemented slightly differently between `BenqiCoreModule` and `BenqiEcosystemModule`.

**BENQI:** Fixed in PR [\#16](https://github.com/aragon/benqi-governance/pull/16).

**Cyfrin:** Verified. The use of `SPEED_PRECISION` has been removed entirely, rather than scaling in subsequent usage as recommended.

\clearpage
