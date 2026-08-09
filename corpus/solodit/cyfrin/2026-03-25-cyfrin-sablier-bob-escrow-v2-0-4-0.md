---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Use read-then-increment in one line
vuln_class: []
---

# Use read-then-increment in one line

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Use read-then-increment in one line:

* `SablierEscrow::createOrder`
```diff
-       orderId = nextOrderId;
-       unchecked {
-           nextOrderId = orderId + 1;
-       }
+       unchecked { orderId = nextOrderId++; }
```

* `SablierBob::createVault`
```diff
-       vaultId = nextVaultId;
-       unchecked {
-           nextVaultId = vaultId + 1;
-       }
+       unchecked { vaultId = nextVaultId++; }
```

**Sablier:** Acknowledged.
