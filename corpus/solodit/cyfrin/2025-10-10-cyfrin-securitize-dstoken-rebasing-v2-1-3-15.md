---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-15
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
title: Refactor away duplicated code between `ComplianceService::newPreTransferCheck`
  and `preTransferCheck`
vuln_class: []
---

# Refactor away duplicated code between `ComplianceService::newPreTransferCheck` and `preTransferCheck`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** `ComplianceService::newPreTransferCheck` and `preTransferCheck` do exactly the same thing, the only difference is that:
* `newPreTransferCheck` takes `balanceFrom` and `paused` as input parameters
* `preTransferCheck` doesn't and has to look them up

So to remove code duplication, `preTransferCheck` should call `newPreTransferCheck` with the parameters it looks up eg:
```solidity
    function preTransferCheck(
        address _from,
        address _to,
        uint256 _value
    ) public view virtual override returns (uint256 code, string memory reason) {
        IDSToken token = getToken();
        return newPreTransferCheck(_from, _to, _value, token.balanceOf(_from), token.isPaused());
    }
```

**Securitize:** Fixed in commit [3b1894a](https://github.com/securitize-io/dstoken/commit/3b1894af9b02fc10f41dd697122f6339db518d2f).

**Cyfrin:** Verified.
