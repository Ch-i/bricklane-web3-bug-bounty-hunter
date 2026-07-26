---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-2-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: 'Missing events: constructor init event absent and admin-mutating events lack
  msg.sender'
vuln_class: []
---

# Missing events: constructor init event absent and admin-mutating events lack msg.sender

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of events-related observability gaps. Each sub-item is a distinct instance.

---

**1. Admin-mutating events lack `msg.sender` attribution**

`IsWorkflowIdValidUpdated`, `ForwarderAddressUpdated`, and other admin-mutating events in `ChainlinkReceiverBase` do not emit the caller. Audit trail limited.

**Recommended:** Add `address indexed caller` (= `msg.sender`) to every admin-mutating event.

---

**2. Constructor does not emit an initialization event**

`ChainlinkAdapter` constructor does not emit an event recording `VERIFIER_PROXY` or `CTF`. Off-chain indexers cannot identify these without reading storage or parsing constructor args.

**Recommended:** Emit `ChainlinkAdapterInitialized(address verifierProxy, address ctf)` in the constructor.

---

**Predict.fun:** Fixed in commit [4ba7df](https://github.com/PredictDotFun/prediction-market/pull/71/changes/4ba7dfd6f9ac298befcd0594c3e26371d07fce3d).

**Cyfrin:** Verified.
