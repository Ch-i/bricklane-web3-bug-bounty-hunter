---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-12-cyfrin-shutter-security-council-v2-0-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-12-cyfrin-shutter-security-council-v2-0
title: '`timelockPeriod` documented as seconds but `Azorius` treats it as blocks,
  causing ~36-day timelock'
vuln_class: []
---

# `timelockPeriod` documented as seconds but `Azorius` treats it as blocks, causing ~36-day timelock

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-12-cyfrin-shutter-security-council-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-12-cyfrin-shutter-security-council-v2.0.md)_

---

**Description:** The [GOVERNANCE_PARAMETERS.md:139](https://github.com/Cyfrin/audit-2026-03-shutter-security-council-src/blob/94736af/Shutter-Security-Council/docs/GOVERNANCE_PARAMETERS.md#L139) states that `timelockPeriod` is in seconds and uses `block.timestamp` comparison. The actual `Azorius` code compares it against `block.number`, meaning `timelockPeriod` is in blocks.

The recommended value of `259,200` is calibrated as seconds (3 days), but `Azorius` adds it to `votingEndBlock` and compares against `block.number`. At `12s` average block time, `259,200` blocks equals ~36 days, not 3 days.

[Azorius.sol#L317-L328](https://github.com/Cyfrin/audit-2026-03-shutter-security-council-src/blob/94736af/Shutter-Security-Council/src/azorius/Azorius.sol#L317-L328)
```solidity
uint256 votingEndBlock = _strategy.votingEndBlock(_proposalId);

// ...

} else if (block.number <= votingEndBlock + _proposal.timelockPeriod) {
    return ProposalState.TIMELOCKED;
```

[GOVERNANCE_PARAMETERS.md#L139](https://github.com/Cyfrin/audit-2026-03-shutter-security-council-src/blob/94736af/Shutter-Security-Council/docs/GOVERNANCE_PARAMETERS.md#L139)

`timelockPeriod` is in seconds, not blocks. It uses `block.timestamp` comparison.
For reference, `executionPeriod` is correctly documented as blocks, and its recommended value of `50,400` blocks correctly equals ~7 days at 12s block time.

**Impact:** If the deployment follows the markdown as-is, governance proposals will be locked for ~36 days instead of the intended 3 days after passing a vote. This makes the DAO nearly unusable and proposals would likely expire before reaching the execution window. The correct value for a 3-day timelock is `21,600` blocks (matching the current `votingPeriod` and original `executionPeriod`).

**Recommended Mitigation:** Update `GOVERNANCE_PARAMETERS.md` to correct the unit and value:

- Change timelockPeriod description from "seconds" to "blocks"
- Change the recommended value from `259,200` to `21,600` (3 days in blocks at 12s block time)

**Blockful:** Fixed in commit [76081e2](https://github.com/blockful/shutter-security-council/commit/76081e20a1e668e0ddc794dec2f91c6ccf15e7b2)

**Cyfrin:** Verified. Documentation on `GOVERNANCE_PARAMETERS.md` has been updated to the correct number of blocks for the expected delay time.

\clearpage
