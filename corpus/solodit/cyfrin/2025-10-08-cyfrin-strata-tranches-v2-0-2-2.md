---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: NAVs or APRs are updated using an outdated accounting on certain operations
vuln_class: []
---

# NAVs or APRs are updated using an outdated accounting on certain operations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The next list of functions makes changes either to the NAVs or APRs, or both of them, but none of those variables are updated before the update is reflected on the storage, which means, the accounting is updated using outdated values that don't reflect the current value.

- `Accounting::setReserveBps()`
- `Accounting::setRiskParameters()`
- `Accounting::reduceReserve()`
- `Accounting::updateAprs()`
- `Accounting::onAprChanged()`

For example, when reducing reserves, the `reserveNav` and `nav` are updated, but those variables were not previously updated, which means that the update to `reserveNav` and `nav` is made on outdated values since the last time those navs were updated.
- Since the last update, the `sUSDe <=> USDe rate` could've changed, but that difference is not reflected on the navs prior to updating them to subtract the amount by which the reserves are been reduced.

Another example is when updating APRs:
- If the APR is lowered, SR Tranche will loss on rewards because the lower APR will be applied to a higher time period.
- If the APR is increased, JR Tranche will loss on profits because the higher APR will be applied to a higher time period benefiting the SR Tranche at the expense of the JR Tranche.

**Impact:** Update of accounting with outdated data can result in unexpected outcomes and potentially messing up the accounting for operations afterwards.

Updating APRs without updating the internal accounting causes that the new APR is applied to calculations until an update occurs.
- If the APR was lowered, SR Tranche will loss on rewards because the lower APR will be applied to a higher time period.
- If the APR was increased, JR Tranche will loss on profits because the higher APR will be applied to a higher time period benefiting the SR Tranche at the expense of the JR Tranche.

**Recommended Mitigation:** Consider updating the internal NAVs and APRs prior to making any changes to them on the listed functions in the Description section.

**Strata:**
Fixed in commits [7b2354](https://github.com/Strata-Money/contracts-tranches/commit/7b235498d15274867f74bd84495f227b4e20fa94), [c3c927](https://github.com/Strata-Money/contracts-tranches/commit/c3c927784d6f87582895a9d14ad022d5f5a5d6b8), [cc1172a](https://github.com/Strata-Money/contracts-tranches/commit/cc1172ac20c42f3c4624754a9d4c08dd1ce1634e), [90a7ad](https://github.com/Strata-Money/contracts-tranches/commit/90a7ad3106f44ee988067145aa8737fa0622e9c6), [2cfe69](https://github.com/Strata-Money/contracts-tranches/commit/2cfe69946b21f55a349fff6e67296c8fa6fcecef),  and, [674505](https://github.com/Strata-Money/contracts-tranches/commit/674505f27505f940ec5eefe868ecb389ae8c517f) by refactoring the update to indexes and aprs in two separate actions as well as triggering updates to the accounting prior to use any of the NAVs, and recalculating the aprs when changes to `jrtNav` or `srtNav` occurs.

**Cyfrin:** Verfified.
The system now has a symmetric relationship across operations where:
- internal accounting its updated at the top of the execution.
- whenever a change to `jrtNav` or `srtNav` happens, the apr is re-calculated at the end of the tx.
