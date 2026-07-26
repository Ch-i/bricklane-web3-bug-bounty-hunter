---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: Consider using `Ownable2Step`
vuln_class: []
---

# Consider using `Ownable2Step`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The contract uses OpenZeppelin’s single‑step `Ownable`, where ownership transfers immediately upon `transferOwnership`, risking accidental or unwanted transfers. Consider switching to OZ’s `Ownable2Step`, which requires the new owner to explicitly call `acceptOwnership`. This two‑step pattern prevents mis‑sent or unacknowledged ownership transfers and aligns with best‑practice “Unchecked 2‑Step Ownership Transfer” safeguards.


**Stake.Link:** Acknowledged.
