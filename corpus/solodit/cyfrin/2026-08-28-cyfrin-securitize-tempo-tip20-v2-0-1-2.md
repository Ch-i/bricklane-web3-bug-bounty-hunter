---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-1-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` predicts the TIP-403 policy ID instead of reading the receipt'
vuln_class: []
---

# `deploy-full.ts` predicts the TIP-403 policy ID instead of reading the receipt

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The deployment script obtains the next global TIP-403 policy ID with `staticCall`, sends `createPolicy`, and ignores the transaction result. Another policy creation between those calls changes the assigned ID. The deploy need not abort. `FEEMGR` and `DEX` are hardcoded and public, so whoever won the race can pre-authorize both under their own policy; the next step's guard then skips `addPlatformWallet` entirely. Step 5's registrar failures are swallowed, and the script continues through the handoff and prints DONE.

**Impact:** The registry is bound to a policy it cannot write to, while the race winner administers the whitelist the token enforces. Both `setPolicyId` and `changeTransferPolicyId` take the raced id, so the token points at the attacker's policy too. `setPolicyId` is one-shot and never checks `policyData(id).admin`, so the deployed implementation cannot correct the binding; recovery needs a UUPS upgrade that adds a re-point path, or a redeploy. The deploy can complete and report success in that state.

**Recommended Mitigation:** Read the created policy ID from the mined receipt, then verify its existence, whitelist type, and registry administrator before calling `setPolicyId`.

**Securitize:** Fixed in [PR 15](https://github.com/securitize-io/bc-tempo-sc/pull/15).

**Cyfrin:** Verified.
