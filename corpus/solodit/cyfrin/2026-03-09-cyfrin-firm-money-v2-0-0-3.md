---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-09-cyfrin-firm-money-v2-0-0-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-09-cyfrin-firm-money-v2-0
title: Empty SP removes the entire liquidator incentive
vuln_class: []
---

# Empty SP removes the entire liquidator incentive

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-09-cyfrin-firm-money-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-09-cyfrin-firm-money-v2.0.md)_

---

**Description:** The protocol sets `ETH_GAS_COMPENSATION = 0` ([Constants.sol:14](https://github.com/firm-money/firm/blob/main/contracts/src/Dependencies/Constants.sol#L14)).

The remaining collateral compensation is only calculated inside the SP offset path at [TroveManager.sol:378-382](https://github.com/firm-money/firm/blob/main/contracts/src/TroveManager.sol#L378-L382).
When the SP is nearly empty, most of the liquidation goes through redistribution where `collGasCompensation` stays at its default value of 0.

**Impact:** During drastic market conditions that drain the SP, liquidators receive zero compensation. The protocol relies solely on trove owners liquidating to prevent bad debt redistribution onto their own positions, an indirect and unreliable incentive during the most critical moments.

**Recommended Mitigation:** Extend the collateral gas compensation calculation to the redistribution path so liquidators always receive a baseline reward regardless of SP state, similar to LiquityV1 liquidation design.

**Firm Money:**
Acknowledged. Since Status is a gasless chain, theres no cost for us to process the liquidation or redistribution. We'll already be running liquidation bots so I dont foresee this being an issue even in extreme circumstances. The UX benefits for not having a gas deposit are huge.
