---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-13
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaWindDown::governanceTriggerWindDown` selector unregistered, force-classified
  Extended instead of spec-mandated Standard'
vuln_class: []
---

# `ArmadaWindDown::governanceTriggerWindDown` selector unregistered, force-classified Extended instead of spec-mandated Standard

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `GOVERNANCE.md:618, 622-624` lists the wind-down trigger as governable via "standard proposal". `ArmadaGovernor::initialize` (`contracts/governance/ArmadaGovernor.sol:339-417`) registers neither `governanceTriggerWindDown()` in `standardSelectors` nor in `extendedSelectors`. `_classifyProposal` at `contracts/governance/ArmadaGovernor.sol:1160` fail-closes unrecognized selectors to Extended:

```solidity
// Fail-closed: unrecognized selectors force Extended classification.
if (!standardSelectors[selector]) return ProposalType.Extended;
```

A `propose([armadaWindDown.governanceTriggerWindDown()])` call therefore force-classifies Extended.

**Impact:** Governance-initiated wind-down trigger runs at the Extended bar (14-day vote, 30% quorum, 7-day execution delay) instead of the spec-mandated Standard bar (7-day vote, 20% quorum, 2-day execution delay). End-to-end ~16 days vs ~9 days, with a wider voting coalition required. The permissionless `triggerWindDown()` path (after deadline elapsed and revenue threshold unmet) remains unaffected, so wind-down is never blocked - only slower than promised when initiated via governance.

**Recommended Mitigation:** Register the selector in `standardSelectors` during `initialize`:

```diff
+ standardSelectors[bytes4(keccak256("governanceTriggerWindDown()"))] = true;
```

Alternatively, update `GOVERNANCE.md:618, 622-624` to classify the wind-down trigger as Extended if the team prefers the higher consensus bar for an irreversible action.

**Armada:** Fixed in commit [91d6d59](https://github.com/ship-armada/armada-poc/commit/91d6d594b6583e0a870a13c3013b139fc647ad65) - we chose to go with the current implementation keeping it as Extended and update the spec.

**Cyfrin:** Verified.
