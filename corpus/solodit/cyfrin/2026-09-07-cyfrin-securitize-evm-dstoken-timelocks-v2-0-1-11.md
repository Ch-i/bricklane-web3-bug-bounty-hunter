---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-11
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: Minting-control documentation is stale on window reset and silent on exceptional-mint
  operations and the tumbling-window boundary
vuln_class: []
---

# Minting-control documentation is stale on window reset and silent on exceptional-mint operations and the tumbling-window boundary

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** Three gaps between the shipped BC-2132 documents and the code:

1. `docs/bc-2132-mint-throttling-flows.md` Flow 14 says `setMintCap` does not reset the window. `DSToken::setMintCap` resets `windowStart` and `mintedInWindow` on every call, as the `MintCapUpdated` NatSpec states.
2. `docs/runbooks/governance-timelocks.md` has no exceptional-mint section: no procedure for scheduling or for cancelling through the master queue after handover, no `OverCapMintScheduled`, `OverCapMintExecuted`, `OverCapMintCancelled` in Monitoring (although `timelocks.md` section 5 assumes they are indexed), and no step to set `overCapDelay` and `overCapGracePeriod` before `setMintCap` enables the cap, both of which default to 0.
3. The tumbling-window boundary is undocumented. `DSToken::_checkThrottle` re-anchors `windowStart` to the triggering call, so an ISSUER can mint `mintCapAmount` just before expiry and again just after: `2 * mintCapAmount` within seconds at any boundary. The long-run rate is unchanged, so this is a property of the FR-7 design, but `timelocks.md` section 8 asks for the maximum per window and no document states it.

**Impact:** Operators working from the flows doc expect a window that survives a cap change; those working from the runbook get no procedure, no events to index and no instruction to configure the delay and grace period before enabling the cap, so the exceptional path can go live with both at 0. The boundary property means the real per-window ceiling is `2 * mintCapAmount`, not `mintCapAmount`, and nothing tells the client that.

**Recommended Mitigation:** Correct Flow 14. Add an exceptional-mint section to the runbook covering scheduling, cancellation via the master queue, the three events, and the configuration order. State the `2 * mintCapAmount` boundary property in FR-7 and the flows doc; if the intent is "at most `mintCapAmount` in any `mintCapWindow` interval", the throttle needs sliding-window accounting.

**Securitize:** Fixed in commit [60ff14a](https://github.com/securitize-io/dstoken/commit/60ff14ac609b32e191a53654ffce4578902decc3).

**Cyfrin:** Verified. All three items are documented correctly and match the merged code.


\clearpage
