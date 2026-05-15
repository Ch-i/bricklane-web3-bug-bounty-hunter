---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Revert fast by performing input related checks prior to storage reads and external
  calls
vuln_class: []
---

# Revert fast by performing input related checks prior to storage reads and external calls

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Revert fast by performing input related checks prior to storage reads and external calls:
* `SablierBob::enter` - perform `amount` check first
* `SablierLidoAdapter::updateStakedTokenBalance` - perform `userShareBalanceBeforeTransfer` check first

**Sablier:** Fixed in commit [0b2ea33](https://github.com/sablier-labs/lockup/commit/0b2ea3320e6ced340588c916d53713e0ce98136e).

**Cyfrin:** Verified.
