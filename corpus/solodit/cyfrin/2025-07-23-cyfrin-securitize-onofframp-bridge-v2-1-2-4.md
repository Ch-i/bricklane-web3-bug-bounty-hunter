---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Single-step ownership transfer pattern is not recommended
vuln_class: []
---

# Single-step ownership transfer pattern is not recommended

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The two `BaseContract` implementations currently inherit from OpenZeppelin's `OwnableUpgradeable`, which uses a **single-step ownership transfer** pattern. This approach is risky: if an incorrect address is set as the new owner, the contract may become permanently inaccessible to administrative functions (`onlyOwner` methods).

**Impact:** A misconfigured ownership transfer could lock critical administrative functionality, potentially disrupting operations or requiring emergency upgrades.

**Recommended Mitigation:** Adopt the **Ownable2StepUpgradeable** contract from OpenZeppelin. This two-step ownership transfer pattern ensures the new owner must explicitly accept the role, reducing the risk of accidental lockouts.

```diff
-abstract contract BaseContract is UUPSUpgradeable, PausableUpgradeable, OwnableUpgradeable {
+abstract contract BaseContract is UUPSUpgradeable, PausableUpgradeable, Ownable2StepUpgradeable {
```

**Securitize:** Acknowledged.

**Cyfrin:** Acknowledged.
