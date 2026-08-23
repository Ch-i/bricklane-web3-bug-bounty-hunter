---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-ethcf-swapboard-v2-0-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-ethcf-swapboard-v2-0
title: Cache storage to prevent identical storage reads
vuln_class: []
---

# Cache storage to prevent identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-ethcf-swapboard-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-ethcf-swapboard-v2.0.md)_

---

**Description:** In EVM reading from storage is expensive; cache storage to prevent identical storage reads when known values can't change:
* `fillOrder, cancelOrder` - cache `order.maker`
* `fillOrderWithEth` - cache `order.maker, order.amountB`
* `cancelOrderUnwrap, fillOrderUnwrap` - cache `order.maker, order.amountA`

**ETHCF:** Fixed in commits [572f3c5](https://github.com/ETHCF/swapboard/commit/572f3c5d724b78fc3a2f304557a23c018f9fc31d), [3a9e06e](https://github.com/ETHCF/swapboard/commit/3a9e06eb2493b0c501b484c05e3d1033d7e56ba2).

**Cyfrin:** Verified.
