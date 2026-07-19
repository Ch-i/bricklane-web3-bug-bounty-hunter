---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`BlacklistableUpgradeable` uses single-step `OwnableUpgradeable` — instant
  ownership transfer bypasses all `owner()`-gated invariants'
vuln_class: []
---

# `BlacklistableUpgradeable` uses single-step `OwnableUpgradeable` — instant ownership transfer bypasses all `owner()`-gated invariants

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `issuance/src/helpers/BlacklistableUpgradeable.sol:10`, `issuance/src/token/HilToken.sol:169,211`

`BlacklistableUpgradeable` inherits OZ's `OwnableUpgradeable` (single-step), not `Ownable2StepUpgradeable`. The `owner()` role carries elevated privileges in every HilToken derivative:

- `burnFrom`: allowance check skipped when `msg.sender == owner()` (design intent — regulatory confiscation)
- `_update`: `owner()` bypasses the blacklist check for all transfers; the force-transfer (`pendingTransfer`) branch is only reachable when `msg.sender == owner()`

Because `transferOwnership(newOwner)` is instant, a compromised blacklister key can hand `owner()` to an attacker in a single transaction with no waiting period — the attacker immediately inherits both the `burnFrom` allowance-skip and the `_update` force-transfer capability. Separately, `renounceOwnership()` sets `owner()` to `address(0)`, permanently breaking the force-transfer mechanism and the `burnFrom` admin path with no recovery path short of an upgrade.

This is asymmetric with how the rest of the protocol protects sensitive roles: `MINTER_ROLE`, `DISTRIBUTOR_ROLE`, and `CUSTODIAN_ROLE` all use explicit 2-step request/execute patterns with ≥1-day waits, yet the `owner()` role — which can force-burn any holder's balance — has no such protection.

**Impact:** Under a compromised owner key, instant handoff to an attacker who can force-burn any holder's tokens or execute force-transfers without waiting period. `renounceOwnership()` permanently disables force-transfer and the `burnFrom` admin path. Requires malicious or negligent admin.

**Recommended Mitigation:** Replace `OwnableUpgradeable` with `Ownable2StepUpgradeable` so `transferOwnership` only nominates the new owner and requires `acceptOwnership()`. Override `renounceOwnership()` to revert, since removing the owner is irreversible and breaks core token mechanics. Consider extending the 2-step waiting period to match other role setters (≥1 day).

**Syntetika:** Fixed in commit [`536b5d3`](https://github.com/SyntetikaLabs/monorepo/commit/536b5d39ef011442ca88f036be7d76767e7e341a)

**Cyfrin:** Verified.
