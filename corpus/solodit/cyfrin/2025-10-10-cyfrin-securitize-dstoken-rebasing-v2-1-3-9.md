---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: '`TransactionRelayer` and `SecuritizeSwap` should use `CommonUtils::encodeString`'
vuln_class: []
---

# `TransactionRelayer` and `SecuritizeSwap` should use `CommonUtils::encodeString`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `TransactionRelayer::toBytes32` duplicates functionality already available in `CommonUtils::encodeString`; remove the duplicated code and use `CommonUtils::encodeString` instead.

Also this line should use `CommonUtils::encodeString` instead of re-implementing it again:
```solidity
L178:                        keccak256(abi.encodePacked(senderInvestor)),
```

`SecuritizeSwap` also duplicates this functionality:
```solidity
191:                keccak256(abi.encodePacked(_senderInvestorId))
```

**Securitize:** Fixed in commit [1f69125](https://github.com/securitize-io/dstoken/commit/1f691255378a0deba62281755feb3a28339b194e) for `TransactionRelayer`. `SecurtizeSwap` was removed as it was deprecated.

**Cyfrin:** Verified.
