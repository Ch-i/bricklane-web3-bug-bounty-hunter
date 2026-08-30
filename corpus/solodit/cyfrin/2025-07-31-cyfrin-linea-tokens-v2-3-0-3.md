---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-31-cyfrin-linea-tokens-v2-3-0-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-31T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md
tags:
- firm:cyfrin
- report:2025-07-31-cyfrin-linea-tokens-v2-3
title: Consider implementing emergency pause mechanism for user facing calls
vuln_class: []
---

# Consider implementing emergency pause mechanism for user facing calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-31-cyfrin-linea-tokens-v2.3.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-31-cyfrin-linea-tokens-v2.3.md)_

---

**Description:** Both `TokenAirdrop` and `LineaToken` expose critical operations that, once live, cannot be halted in the event of an unforeseen bug or exploit:

* `TokenAirdrop::claim`
  Without a pausable guard, any mis‑calculation or malicious behavior in the “factor” tokens (e.g. a faulty `balanceOf` or overflow/rounding exploit) could irreversibly drain or lock the airdrop pool.


* `LineaToken::syncTotalSupplyToL2`
  This function bridges on‑chain state to L2. If an L2 upgrade introduces a bug, or the message service changes fee semantics, repeated calls could fail or corrupt cross‑chain state without any ability to stop them.

Consider integrating OpenZeppelin’s `Pausable` (`Upgradeable`) so that the owner/admin can halt pause the contracts in case of any critical issues.

**Linea:** Acknowledged. This is intentional to provide users access to their tokens at all times.
