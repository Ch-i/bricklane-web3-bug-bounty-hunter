---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: 'Code hygiene: inconsistent imports, mappings, custom errors, events, and naming'
vuln_class: []
---

# Code hygiene: inconsistent imports, mappings, custom errors, events, and naming

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Enumerated sub-items.

1. Use named imports consistently (e.g. `import {IERC20} from "..."`). Every in-scope file currently uses unnamed imports.

2. Use named mapping parameters (requires pragma bump to 0.8.18+). Examples: `mapping(address participant => mapping(uint8 hop => Participant)) public participants;` in `ArmadaCrowdfund`; `mapping(address inviter => mapping(uint256 nonce => bool)) public usedNonces;`.

3. Inconsistent custom error vs require-string usage. `ArmadaGovernor` uses `Gov_*` custom errors throughout; every other in-scope contract uses `require("...")`. Pick a single convention for the suite (custom errors recommended) and apply uniformly.

4. Magic numeric literals appear inline in arithmetic and comparisons across multiple in-scope contracts; extract them to named constants for readability and audit-traceability. Where the same literal is used across multiple files, define it once in a shared constants file (e.g. `contracts/governance/Constants.sol`) that every consumer imports, rather than redeclaring the same constant in each file.

    - BPS denominator `10000` is used inline 8 times across 3 files: `ArmadaCrowdfund::_computeHopAllocations` at `contracts/crowdfund/ArmadaCrowdfund.sol:759, 763, 764`; `ArmadaGovernor::quorum, _classifyProposal` at `contracts/governance/ArmadaGovernor.sol:1037, 1152`; and `ArmadaTreasuryGov` at `contracts/governance/ArmadaTreasuryGov.sol:244, 301, 459, 580`. Define `uint256 constant BPS_DENOMINATOR = 10_000;` once in a shared constants file and import it in all three contracts.

    - `contracts/crowdfund/ArmadaCrowdfund.sol:164-166` encodes hop policy as raw literals in the constructor `HopConfig` initialisers (`7000`, `4500`, `15_000`, `4_000`, `1_000`). Promote to named constants (e.g. `HOP0_CEILING_BPS = 7000`, `HOP1_CEILING_BPS = 4500`, `HOP0_CAP_USDC = 15_000 * 1e6`, `HOP1_CAP_USDC = 4_000 * 1e6`, `HOP2_CAP_USDC = 1_000 * 1e6`) alongside the existing `BASE_SALE`, `MIN_SALE`, `HOP2_FLOOR_BPS` constants already defined in that file.

    - `RevenueLock::_unlockBpsForRevenue` at `contracts/governance/RevenueLock.sol:260-266` encodes the unlock schedule as paired magic literals (`1_000_000e18`/`10000`, `500_000e18`/`8000`, `250_000e18`/`6000`, `100_000e18`/`4000`, `50_000e18`/`2500`, `10_000e18`/`1000`) without NatSpec declaring that `revenue` is 18-decimal USD. Extract named constants (e.g. `MILESTONE_100_PCT_USD = 1_000_000e18`, `MILESTONE_100_PCT_BPS = 10_000`, etc.) and add a NatSpec block documenting the unit.

5. `ArmadaCrowdfund::ArmLoaded` emits no payload despite being permissionless. Extend to `ArmLoaded(address indexed caller, uint256 balance, uint256 required)`.

6. `ArmadaGovernor::setSecurityCouncil` accepts any address including the current one; a no-op call still emits. Add a same-value guard: `if (oldSC == newSC) revert Gov_NoChange();`.

7. `TreasurySteward::removeSteward` emits before the state write. Cache `removed = currentSteward;`, then clear, then emit.

8. `ArmadaCrowdfund::finalizedAt` is set in both success and refund-mode branches but its NatSpec describes only the success-path semantic. Upgrade the comment to a NatSpec block noting that consumers must check `phase == Phase.Finalized && !refundMode` to distinguish.

9. `ArmadaGovernor::__gap` comment states the wrong slot count; verify and correct to match the declared array size.

**Impact:** Code hygiene; no direct security risk.

**Recommended Mitigation:** Apply the per-subitem mitigations enumerated above.

**Armada:** Fixed some items in commit [7d67f2e](https://github.com/ship-armada/armada-poc/commit/7d67f2ed25d7969350654fa8474f4a3da433cf55), deferred others.

**Cyfrin:** Verified with following notes:
* 5, 6, 7, 8, 9 are fixed
* 4 mostly done except BPS denominator `10000`
* 1, 2, 3 deferred
