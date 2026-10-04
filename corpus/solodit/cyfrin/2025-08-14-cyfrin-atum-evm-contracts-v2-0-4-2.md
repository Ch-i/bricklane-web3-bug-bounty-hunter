---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-4-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Use `calldata` instead of `memory` for read-only function inputs
vuln_class: []
---

# Use `calldata` instead of `memory` for read-only function inputs

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** Use `calldata` instead of `memory` for read-only function inputs where those function inputs are also never passed to functions which receive them as `memory`:
* `Escrow::reserve, release, refund` - both `witness` and `signature`, then call `isValidSignatureNowCalldata` instead of `isValidSignatureNow`

**Atum:**
Fixed in commit [6726871](https://github.com/Atum-Labs/evm-contracts/commit/672687134c9a65cba4c9eb1528c499e80bc80a49). Note that `isValidSignatureNowCalldata` is not available yet in any official OZ release so we haven't used it at this time.

**Cyfrin:** Verified.
