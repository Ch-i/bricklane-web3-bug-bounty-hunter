---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Don't perform storage reads unless necessary
vuln_class: []
---

# Don't perform storage reads unless necessary

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** Reading from storage is expensive; don't perform storage reads unless necessary.

* `contracts/service/ServiceConsumer.sol`
```diff
// in `onlyMaster` don't load trust manager unless required
    modifier onlyMaster {
-        IDSTrustService trustManager = getTrustService();
-        require(owner() == msg.sender || trustManager.getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
+        if(owner() != msg.sender) require(getTrustService().getRole(msg.sender) == ROLE_MASTER, "Insufficient trust level");
        _;
    }
```

**Securitize:** Fixed in commit [1ab6fd9](https://github.com/securitize-io/dstoken/commit/1ab6fd99a2a6814b23ec7e51359ced72159bfe80).

**Cyfrin:** Verified.
