---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Placeholder recipient constants in `Ignite` should be updated before deployment
vuln_class: []
---

# Placeholder recipient constants in `Ignite` should be updated before deployment

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** While it is understood that the [`FEE_RECIPIENT`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L43) and [`SLASHED_TOKEN_RECIPIENT`](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L44) constants in `Ignite` have been modified for testing purposes, it is important to note that they should be reverted to valid values before deployment to ensure that fees and slashed tokens are not lost.

```solidity
address public constant FEE_RECIPIENT = 0xaAaAaAaaAaAaAaaAaAAAAAAAAaaaAaAaAaaAaaAa; // @audit-info - update placeholder values
address public constant SLASHED_TOKEN_RECIPIENT = 0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB;
```

**Recommended Mitigation:** Update the constants before performing the `Ignite` contract upgrade.

**BENQI:** Acknowledged, already in the checklist for deployments.

**Cyfrin:** Acknowledged.
