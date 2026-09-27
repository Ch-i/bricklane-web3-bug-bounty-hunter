---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`DeployDeterministic::run` does not verify the pinned `Factory` release'
vuln_class: []
---

# `DeployDeterministic::run` does not verify the pinned `Factory` release

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `DeployDeterministic::run` hashes the locally compiled `Factory` creation code, predicts an address from that hash, deploys the same creation code, and then requires the returned address to equal the prediction. This equality confirms only that CREATE2 behaved as expected. It holds for any locally compiled creation code and does not establish that the code matches the init-code hash or address pinned for the intended release.

**Impact:** An operator using the wrong source revision, compiler configuration, or linked library address can successfully deploy a `Factory` at an unintended address while every in-script assertion passes. Integrations configured for the release's canonical address will not use that deployment, requiring a corrected deployment and potentially causing operational confusion or cross-chain address drift.

**Recommended Mitigation:** Before broadcasting, require the locally computed init-code hash to equal a release-pinned hash and require the prediction to equal an explicitly supplied or release-pinned expected `Factory` address. Keep these expected values in a versioned deployment artifact rather than deriving both sides of the checks from the current local build.

**GreekFi:** Fixed in [PR32](https://github.com/greekfi/contracts/pull/32)

**Cyfrin:** Verified. The deployment script now checks the locally compiled Factory hash and predicted address against independently pinned release values before broadcasting.
