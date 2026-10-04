---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-13
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-14] Consider escaping data in send_mg function'
vuln_class: []
---

# [I-14] Consider escaping data in send_mg function

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Original severity:** Best Practices

**Files:** [`boring_vault.py`](https://github.com/SwellNetwork/hlp-internal-be/blob/c650a499023489bfa5d6ac027b28a940a3c44cdc/app/domain/boring_vault/service/boring_vault.py#L277)

**Description:**

Dynamic content sent to Telegram lacks proper output encoding, creating potential security risks when data is transmitted to external services. While the current risk is mitigated because the protocol team controls the data sources (smart contracts and internal calculations).

**Impact:** Implementing proper output encoding represents a security best practice that prevents potential injection vulnerabilities.

**Recommendation:** Implement HTML escaping for all dynamic content before transmission to Telegram using `html.escape()`. For example: `html.escape(str(self.boring_vault_address))`.

**Status:** Fixed

**Client response:** Fixed in [361d3ffb8a1dfb0f5517fc21b2f5ff385bc68dfd](https://github.com/SwellNetwork/hlp-internal-be/pull/13/commits/361d3ffb8a1dfb0f5517fc21b2f5ff385bc68dfd).
