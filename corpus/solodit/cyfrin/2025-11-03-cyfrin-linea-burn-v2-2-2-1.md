---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-03-cyfrin-linea-burn-v2-2-2-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-11-03T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md
tags:
- firm:cyfrin
- report:2025-11-03-cyfrin-linea-burn-v2-2
title: Redundant call to sinc LINEA token supply on `L1LineaTokenBurner`
vuln_class: []
---

# Redundant call to sinc LINEA token supply on `L1LineaTokenBurner`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-03-cyfrin-linea-burn-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-03-cyfrin-linea-burn-v2.2.md)_

---

**Description:** `L1LineaTokenBurner::claimMessageWithProof` is in charge of completing the bridge and burn operation of the `RollupRevenueVault` deployed on the L2.

`L1LineaTokenBurner` claims the message on the L1, receives the bridged tokens, and burns them. It can also burn any tokens that are already on the contract.

The redundancy is in calling `LINEA_TOKEN::syncTotalSupplyToL2` each time `L1LineaTokenBurner::claimMessageWithProof` is called, regardless of how much time has passed since the last burn, or how many LINEA tokens were burnt.

Given that `LINEA_TOKEN::syncTotalSupplyToL2` can be called by anyone at any time, and the function uses the current total supply, `L1LineaTokenBurner` can be optimized not to sync the L2 supply on each call.

**Recommended Mitigation:** Consider removing the call to `LINEA_TOKEN::syncTotalSupplyToL2` on the `L1LineaTokenBurner::claimMessageWithProof`; instead, explore alternatives to bundle multiple burns of the LINEA token into a single call to `LINEA_TOKEN::syncTotalSupplyToL2`.
- Define a criterion that determines when the L2 supply should be synced. It can occur after a certain amount of LINEA tokens have been burned, or after a specified time period has passed.

**Linea:** Fixed in commit [43ed33](https://github.com/Consensys/linea-monorepo/pull/1604/commits/43ed33d00873756bb13ab5de5adafeba61d1fd4b)

**Cyfrin:** Verified.

\clearpage
