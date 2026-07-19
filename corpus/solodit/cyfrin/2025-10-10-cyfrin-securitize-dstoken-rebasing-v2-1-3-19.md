---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-3-19
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Remove useless function `ComplianceServiceRegulated::adjustTransferCounts`
vuln_class: []
---

# Remove useless function `ComplianceServiceRegulated::adjustTransferCounts`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The function `ComplianceServiceRegulated::adjustTransferCounts` is useless as it always just calls `adjustTotalInvestorsCounts` with its two parameters; remove it and simply call `adjustTotalInvestorsCounts` direct:
```diff
    function recordTransfer(
        address _from,
        address _to,
        uint256 _value
    ) internal override returns (bool) {
        if (compareInvestorBalance(_to, _value, 0)) {
-            adjustTransferCounts(_to, CommonUtils.IncDec.Increase);
+            adjustTotalInvestorsCounts(_to, CommonUtils.IncDec.Increase);
        }

        if (compareInvestorBalance(_from, _value, _value)) {
            adjustTotalInvestorsCounts(_from, CommonUtils.IncDec.Decrease);
        }

        cleanupInvestorIssuances(_from);
        cleanupInvestorIssuances(_to);
        return true;
    }

-    function adjustTransferCounts(
-        address _from,
-        CommonUtils.IncDec _increase
-    ) internal {
-        adjustTotalInvestorsCounts(_from, _increase);
-    }
```

**Securitize:** Fixed in commit [5e524cd](https://github.com/securitize-io/dstoken/commit/5e524cdb10bffc7c118ad0f19bfed315b098f795).

**Cyfrin:** Verified.
