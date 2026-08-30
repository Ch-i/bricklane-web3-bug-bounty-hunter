---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`TokensHolder::withdraw` + `Distributor::rescueERC20` use raw `transfer` without
  `SafeERC20`'
vuln_class: []
---

# `TokensHolder::withdraw` + `Distributor::rescueERC20` use raw `transfer` without `SafeERC20`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Both functions ignore `transfer`'s return value. For tokens that return `false` on failure without reverting, failures are silent. `TokensHolder` is the sole funds-exit path for vault withdrawals - a silent failure wipes the cooldown record while leaving tokens stuck. `Distributor::rescueERC20` is admin-only but inconsistent with the `safeTransfer`/`safeTransferFrom` used elsewhere in the same files.

Sources: issuance/src/helpers/TokensHolder.sol:34-36; issuance/src/vault/Distributor.sol:142-151.

**Recommended Mitigation:** Use `SafeERC20.safeTransfer`. Add an event to `rescueERC20` for observability.

**Syntetika:** Fixed in commit [`39a1cfd`](https://github.com/SyntetikaLabs/monorepo/commit/39a1cfd142867972c59d20af2bc49ba8062a779a)

**Cyfrin:** Verified.
