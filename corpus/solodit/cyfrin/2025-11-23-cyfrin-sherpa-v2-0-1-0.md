---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Misconfigured decimal scale can skew vault accounting
vuln_class: []
---

# Misconfigured decimal scale can skew vault accounting

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** The vault’s math assumes the same decimal scale as the wrapped asset (USDC, 6 decimals) and as the `globalPricePerShare` fed by ops. While deployment sets `vaultParams.decimals = 6` and the wrapper enforces USDC’s 6 decimals, a misconfiguration will skew conversions.

**Impact:** Configuring the vault with more than 6 decimals can cause incorrect accounting, and follow-on reverts in rebalancing.

**Recommended Mitigation:** Consider locking the vault decimals to 6, same as `SherpaUSD`.

**Sherpa:** Fixed in commit [`1a634e0`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/1a634e0331968ea5a73f38a62ef824da9376ab52)

**Cyfrin:** Verified. `_vaultParams.decimals` now verified to be 6 in the constructor.
