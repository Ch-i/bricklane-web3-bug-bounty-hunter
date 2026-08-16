---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-0-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Accounting on `PaymentSettler` will be corrupted when changing `stablecoin`
  that is used to process payments
vuln_class: []
---

# Accounting on `PaymentSettler` will be corrupted when changing `stablecoin` that is used to process payments

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** The accounting on the `PaymentSettler` will be initialized based on the decimals of the initial stablecoin that is used at the beginning of the system.
The system is capable of [changing the stablecoin that is used for the payments](https://github.com/remora-projects/remora-smart-contracts/blob/audit/Dacian/contracts/PaymentSettler.sol#L195-L198), and, when the stablecoin is changed for a stablecoin with different decimals, all the existing accounting will be messed up because the new amounts will vary from the existing values on the system.

This problem was introduced on the last change when the `PaymentSettler` was introduced to the system. On the previous version, the system correctly handled the decimals of the internal accounting to the decimals of the active stablecoin used for payments.

For example, 100 USD of fees that were generated while the stablecoin had 6 decimals would be only 1 USD if the stablecoin were changed to a stablecoin with 8 decimals.

**Impact:** Accounting on `PaymentSettler` will be corrupted when changing `stablecoin` to different decimals.

**Recommended Mitigation:** See recommendation for C-2.

**Remora:** Fixed in commits [a0b277f](https://github.com/remora-projects/remora-smart-contracts/commit/a0b277fe4a59354f3b3783c4b8c06eb60f5157610), [ced21ba](https://github.com/remora-projects/remora-smart-contracts/commit/ced21ba9758b814eb48a09a5e792aa89cc87e8f5).

**Cyfrin:** Verified.
