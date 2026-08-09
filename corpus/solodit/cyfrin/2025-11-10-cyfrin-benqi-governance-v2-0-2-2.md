---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-10-cyfrin-benqi-governance-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-10T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-10-cyfrin-benqi-governance-v2-0
title: Avoid return statements with named return variables
vuln_class: []
---

# Avoid return statements with named return variables

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-10-cyfrin-benqi-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-10-cyfrin-benqi-governance-v2.0.md)_

---

**Description:** When declaring named return variables such as in `GaugeRegistrar::registerGauge`, it is not necessary to explicitly execute the return statement and this can be removed to save gas.

**Recommended Mitigation:**
```diff
function registerGauge(
    address _qiToken,
    Incentive _incentive,
    address _rewardController,
    string calldata _metadataURI
) external auth(GAUGE_REGISTRAR_ROLE) returns (address gaugeAddress) {
    ...
    // Emit event
    emit GaugeRegistered(gaugeAddress, _qiToken, _incentive, _rewardController);
-
-   return gaugeAddress;
}
```

**BENQI:** Acknowledged.

**Cyfrin:** Acknowledged.
