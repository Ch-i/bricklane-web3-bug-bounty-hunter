---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: In `Bet::accept,resolve,cancel` update `Bet` state prior to external calls
vuln_class: []
---

# In `Bet::accept,resolve,cancel` update `Bet` state prior to external calls

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** It is wise to follow the Checks-Effects-Interactions [[1](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html), [2](https://docs.soliditylang.org/en/v0.6.11/security-considerations.html)] pattern; in `Bet::accept,resolve,cancel` the following storage updates should occur prior to making external calls:
```solidity
// `Bet::accept`
_bet.status = IBet.Status.ACTIVE;

// `Bet::resolve`
_bet.winner = winner;
_bet.status = IBet.Status.RESOLVED;

// `Bet::cancel`
_bet.status = IBet.Status.CANCELLED;
```

**WannaBet:** Fixed in commit [5cda880](https://github.com/gskril/wannabet-v2/commit/5cda88027d6081007642caf56dae49af5d753f41).

**Cyfrin:** Verified.
