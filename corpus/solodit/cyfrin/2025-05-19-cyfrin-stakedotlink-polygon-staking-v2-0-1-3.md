---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-1-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: '`disableInitializers` not used to prevent uninitialized contracts'
vuln_class: []
---

# `disableInitializers` not used to prevent uninitialized contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** `PolygonVault` and `PolygonStrategy` contracts are designed to be upgradeable.

They are both inheriting from `Initializable` but do not have a constructor that calls `_disableInitializers()`.

An uninitialized contract can be taken over by an attacker. This applies to both a proxy and its implementation contract, which may impact the proxy. To prevent the implementation contract from being used, `_disableInitializers()` should be called in the constructor to automatically lock it when it is deployed.

**Impact:** Missing constructor with `_disableInitializers()` in `PolygonVault` and `PolygonStrategy` risks unauthorized takeover of uninitialized upgradeable contracts.

**Recommended Mitigation:** Consider adding a constructor to `PolygonVault` and `PolygonStrategy` that explicitly calls `_disableInitializers()`.

**Stake.Link:** Resolved in [PR 151](https://github.com/stakedotlink/contracts/pull/151/commits/7278d0babbf495fb593d1c1e9d827d3d26d94d53)

**Cyfrin:** Resolved.

\clearpage
