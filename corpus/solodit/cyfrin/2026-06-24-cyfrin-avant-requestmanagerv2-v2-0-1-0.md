---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-24-cyfrin-avant-requestmanagerv2-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-24-cyfrin-avant-requestmanagerv2-v2-0
title: '`RequestsManagerV2::cancelBurn` reverts during a pause longer than `burnCancelWindow`,
  breaking the documented pause-cancellation invariant'
vuln_class: []
---

# `RequestsManagerV2::cancelBurn` reverts during a pause longer than `burnCancelWindow`, breaking the documented pause-cancellation invariant

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-24-cyfrin-avant-requestmanagerv2-v2.0.md)_

---

**Description:** The `pause` NatSpec states that _"cancellation paths stay enabled so pending requests can always be unwound while paused"_ (src/RequestsManagerV2.sol:155-156). This holds for `cancelMint`, which has no window or TTL gate and is always callable while CREATED. It does not hold for `cancelBurn`: that function reverts `BurnCancelWindowClosed` once `block.timestamp > createdAt + burnCancelWindow` (src/RequestsManagerV2.sol:362-369). The cancel window is measured against wall-clock `block.timestamp` and keeps elapsing during a pause - the pause does not freeze time. Because `completeBurn` carries `whenNotPaused`, it is unavailable during the pause as well.

If the contract is paused continuously for longer than a pending burn's remaining cancel window (deployed `burnCancelWindow` is 2 days), the provider can neither complete (the contract is paused) nor cancel (the window has closed). The documented _"always be unwound while paused"_ guarantee is false for the burn path: the provider's only self-service exit is gone precisely while the protocol is paused, which is when a user most wants out. The escrowed issue tokens are recoverable only through the admin-gated `adminCancelBurn`, which has no window or pause gate.

**Recommended Mitigation:** Update the NatSpec above `RequestsManagerV2::pause` to correct the false claim that "pending requests can always be unwound while paused" - this is only true for mints but not burns.

**Avant:** Fixed in commit [f7d9275](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/f7d92759a71701a3a941991d57bfdf29c836c040).

**Cyfrin:** Verified.
