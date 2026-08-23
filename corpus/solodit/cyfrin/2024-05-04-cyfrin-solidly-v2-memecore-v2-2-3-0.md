---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-3-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: Cache domain separator and only recompute if the chain ID has changed
vuln_class: []
---

# Cache domain separator and only recompute if the chain ID has changed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

For greater gas efficiency, it is recommended that the current chain ID be cached on contract creation and that the domain separator be recomputed only if a change of chain ID is detected (i.e., ` block.chainid` != cached chain ID). An example can be seen in the implementation of [`Solmate::ERC20`](https://github.com/transmissions11/solmate/blob/c892309933b25c03d32b1b0d674df7ae292ba925/src/tokens/ERC20.sol).

**Solidly Labs:** Acknowledged.

**Cyfrin:** Acknowledged.
