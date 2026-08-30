---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-19-cyfrin-bunni-fee-override-hooklet-v2-0
title: Lack of multicall support for `FeeOverrideHooklet::setFeeOverride`
vuln_class: []
---

# Lack of multicall support for `FeeOverrideHooklet::setFeeOverride`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-19-cyfrin-bunni-fee-override-hooklet-v2.0.md)_

---

**Description:** `FeeOverrideHooklet::setFeeOverride` relies on `msg.sender` when validating ownership of the corresponding `BunniToken`; however, this will be incorrect when invoked through a multicaller contract and cause validation to fail even if the original caller is the actual owner.

Given that any account is free to deploy a Bunni pool and `LibMulticaller` is used heavily throughout the core Bunni contracts, it may be desirable to allow the owner of the pool to perform batched actions on both the hooklet and Bunni itself.

**Impact:** Any legitimate pool owner interacting with the `FeeOverrideHooklet` via a multicaller contract will be incorrectly prevented from doing so, potentially breaking external compatibilities that rely on multicall support.

**Recommended Mitigation:** Replace direct usage of `msg.sender` with `LibMulticaller::senderOrSigner` to remain consistent with the core Bunni contracts. This approach preserves compatibility with both direct and batched calls, ensuring proper access control while supporting multicall infrastructure.

**Bacon Labs:** Fixed in commit [9cf16a8](https://github.com/Bunniapp/hooklets/commit/9cf16a8400f25f5f9eeb2837915c76adc6dc4f54).

**Cyfrin:** Verified. `FeeOverrideHooklet::setFeeOverride` is now compatible with multicall invocations.
