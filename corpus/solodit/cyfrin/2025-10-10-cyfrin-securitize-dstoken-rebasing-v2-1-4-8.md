---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Cheaper not to cache `calldata` array length
vuln_class: []
---

# Cheaper not to cache `calldata` array length

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** It is [cheaper](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#6-dont-cache-calldata-length-effective-009-cheaper) not to cache `calldata` array length:
* `BulkBalanceChecker::getTokenBalances`

**Securitize:** Fixed in commit [fd6eb3b](https://github.com/securitize-io/dstoken/commit/fd6eb3bc4b075ec5975bc8d05305bfcdda054847).

**Cyfrin:** Verified.
