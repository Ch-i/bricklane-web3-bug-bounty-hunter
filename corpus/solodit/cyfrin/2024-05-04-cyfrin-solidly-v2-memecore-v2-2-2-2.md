---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Secondary markets for LP tokens are problematic
vuln_class: []
---

# Secondary markets for LP tokens are problematic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** Unlike other AMM implementations, where fees are accrued in the LP token, Solidly V2 implements an accrual system where the fees are tracked in `feeGrowthGlobal0`/`1` per LP token. Each liquidity provider can call `SolidlyV2Pair::claimFees` to collect their accrued fees, with the benefit being that a liquidity provider does not have to burn their position to access the fees they have accrued.

Fee accrual is synced with every action that changes the balance: when claiming fees, mints, locks, and, most importantly, on any transfer of LP tokens or locked or burnt positions. This means that the fees accrued are bound to the account holding the liquidity position at that time.

Therefore, if these tokens are traded or used as collateral on secondary markets, the fees accrued while in escrow would be lost as these contracts cannot, without modification and knowledge of the Solidly V2 Memecore system, claim fees.

**Impact:** Using Solidly V2 Memecore LP tokens in AMMs, such as within Solidly V2 itself, or different escrow/collateral style contracts will cause fees to be lost.

**Recommended Mitigation:** Be clear about this behavior in the documentation. For the LP tokens to be safely used in a pool of any sort, these would need an ERC-4626-style wrapper vault to be developed. The locked/burnt positions are not so concerning as they would need a custom-built implementation to be traded anyway, which would cater to this in its development..

**Solidly Labs:** Acknowledged. Secondary markets for memecoin LPs are close to non-existent anyway. The most important functions with meme LP tokens are directly available in the core contracts.

**Cyfrin:** Acknowledged.
