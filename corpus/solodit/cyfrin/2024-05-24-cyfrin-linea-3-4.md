---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-3-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Emit event in `MessageServiceBase::_setRemoteSender` when updating `remoteSender`
  storage
vuln_class: []
---

# Emit event in `MessageServiceBase::_setRemoteSender` when updating `remoteSender` storage

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Emit event in `MessageServiceBase::_setRemoteSender` when updating `remoteSender` storage.

**Linea:**
Acknowledged; may be included in a future release. `MessageServiceBase::_setRemoteSender` will only ever be used again on new testnet chains and will not be usable for existing Sepolia and Mainnet deploys.
