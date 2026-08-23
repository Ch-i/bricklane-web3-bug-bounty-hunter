---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-15-cyfrin-story-ip-derivative-agent-v2-1-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md
tags:
- firm:cyfrin
- report:2026-01-15-cyfrin-story-ip-derivative-agent-v2-1
title: Fee-on-transfer ERC20 tokens not supported
vuln_class: []
---

# Fee-on-transfer ERC20 tokens not supported

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md)_

---

**Description:** `IPDerivativeAgent::registerDerivativeViaAgent` assumes the fee token is transferred 1:1. It pulls `tokenAmount` from the caller via `transferFrom`, then later the Royalty Module pulls the required minting fee from the agent via `transferFrom`.

For fee-on-transfer/deflationary ERC20s, the agent may receive less than `tokenAmount` on the initial transfer, causing the subsequent Royalty Module pulls to fail due to insufficient balance (and the derivative registration to revert).

Consider restricting fee tokens to non–fee-on-transfer ERC20s, or if add a parameter `amountIn`, transfer this and measure the agent’s received balance delta and only proceed/approve when it covers the required fee, while refunding the delta.


**Story:** Acknowledged.
