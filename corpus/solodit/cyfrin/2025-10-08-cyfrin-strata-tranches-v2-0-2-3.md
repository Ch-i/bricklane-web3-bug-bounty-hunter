---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Proxy reuse without implementation check inside `UnstakeCooldown` leads to
  execution on outdated/vulnerable logic
vuln_class: []
---

# Proxy reuse without implementation check inside `UnstakeCooldown` leads to execution on outdated/vulnerable logic

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The contract reuses old proxies from the user’s `UnstakeCooldown::proxiesPool` without verifying whether those proxies were created from the current implementation. Since a clone’s target implementation is permanently embedded in its bytecode, if the owner updates `implementations[token]` using the available `UnstakeCooldown::setImplementations`, any proxies already in a user’s pool will still delegate to the old implementation.

**Impact:** Users may continue operating through outdated or vulnerable implementations even after the owner updates `implementations`. This can cause:
- Inconsistent behavior across requests (some proxies use the new implementation, others use the old one).
- Security risks if the previous implementation contains a bug or vulnerability.
- Accounting or logic mismatches if old and new implementations are not compatible.

**Proof of Concept:**
1. Owner sets `implementations[token] = ImplV1`.
2. Alice makes two transfers, creating two proxies that point to `ImplV1`.
3. Owner later calls `setImplementations(token, ImplV2)`.
4. Some time passes, the two proxies pointing to `ImplV1` are available.
5. Alice makes another transfer. The contract pops a proxy from her pool and reuses it.
6. That proxy still delegates to `ImplV1`, even though `implementations[token]` is now `ImplV2`.

**Recommended Mitigation:** When reusing proxies, verify that the proxy’s implementation matches the current `implementations[token]`. If not, discard the old proxy and create a new one.

**Strata:**
Fixed in commit [ffbedf48d](https://github.com/Strata-Money/contracts-tranches/commit/ffbedf48d268f2617e189cddc1daa167220082b3) by implementing a validation to check if the current implementation for a token is different than the implementation that was used to create a proxy being reused. If so, then a new proxy is made with the new implementation, and the old proxy is discarded.

**Cyfrin:** Verified.
