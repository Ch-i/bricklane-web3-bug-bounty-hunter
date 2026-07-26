---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-1-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaGovernor::queue, execute` don''t gate on `windDownActive`, allowing
  in-flight proposals to complete after wind-down'
vuln_class: []
---

# `ArmadaGovernor::queue, execute` don't gate on `windDownActive`, allowing in-flight proposals to complete after wind-down

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::queue, execute` (`contracts/governance/ArmadaGovernor.sol:903-940, 943-970`) only check proposal lifecycle state. Only `propose` and `proposeStewardSpend` block on `windDownActive`. Any proposal that reached `Succeeded` before `ArmadaWindDown::_executeWindDown` flipped `windDownActive` can still be queued and executed afterward.

For `ProposalType.Steward`, the per-execution checks (`stewardContract != address(0)`, `proposer == currentSteward`, `isStewardActive()`) all keep returning true after wind-down because `_executeWindDown` does not call `TreasurySteward::removeSteward` or zero `currentSteward`; `isStewardActive()` then stays true until the 180-day term expires.

**Impact:** Two invariant violations stem from the same missing gate:

1. `GOVERNANCE.md:671` ("Governance is permanently disabled. ... The steward role is void.") is broken - Succeeded steward proposals can be queued and executed after wind-down activates.

2. `distribute` or `stewardSpend` proposals targeting ARM that were Succeeded pre-trigger can execute post-trigger and move ARM out of the treasury. This (a) violates `GOVERNANCE.md:632` ("Treasury ARM has no distribution mechanism after wind-down - it remains locked permanently"), and (b) breaks redemption sequential correctness (`GOVERNANCE.md:651`) because `ArmadaRedemption::circulatingSupply` (`contracts/governance/ArmadaRedemption.sol:196-203`) reads `armToken.balanceOf(treasury)` live; a mid-sequence treasury ARM drop grows `circulatingSupply` and shrinks the per-ARM share for every subsequent redeemer, so late redeemers receive materially less than early ones.

**Recommended Mitigation:** Gate both functions on `windDownActive`:

```diff
function queue(uint256 proposalId) external {
+   if (windDownActive) revert Gov_GovernanceEnded();
    if (state(proposalId) != ProposalState.Succeeded) revert Gov_NotSucceeded();
    ...
}

function execute(uint256 proposalId) external payable nonReentrant {
+   if (windDownActive) revert Gov_GovernanceEnded();
    if (state(proposalId) != ProposalState.Queued) revert Gov_NotQueued();
    ...
}
```

**Armada:** Fixed in commit [a0ff412](https://github.com/ship-armada/armada-poc/commit/a0ff412cb9a5055d02ccfb477548413d63a70a2c).

**Cyfrin:** Verified.
