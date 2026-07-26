---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-8
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Attacker can exploit Dividend allocation by depositing large mounts of DRVS
  Tokens
vuln_class: []
---

# Attacker can exploit Dividend allocation by depositing large mounts of DRVS Tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** Dividends can be allocated once every hour, and the allocation process can be triggered by anyone. The distribution of fees is determined based on the amount of DRVS tokens each user has deposited at the time of allocation.

However, since the allocation timing is predictable, an attacker can exploit this mechanism by depositing a large amount of DRVS tokens just before the allocation occurs. This allows the attacker to unfairly receive a portion of the dividends that should rightfully belong to long-term depositors. Immediately after receiving their share of the dividends, the attacker can claim and then withdraw their DRVS tokens, effectively capturing profits without making any meaningful contribution to the system.

This behavior can be further optimized. For example, an attacker could develop a smart contract that performs all the steps deposit, trigger the allocation, and withdraw within a single transaction.

An attacker doesn’t need to hold DRVS at all in wallet — they can simply use a flash loan to temporarily acquire the dividend, claim the dividend. Similarly, they can borrow DRVS, claim the rewards, and return the borrowed amount, or just swap another asset into DRVS to claim the dividend and immediately swap back.

**Impact:** This allows repeated exploitation of the allocation mechanism, letting attackers drain dividends from honest users and reducing the fairness of the distribution process.

**Recommended Mitigation:** Mitigations are:
1. Introduce a withdrawal delay — users should only be allowed to withdraw their DRVS tokens after a certain period has passed since their last deposit.
2. Reduce the allocation interval — allow allocations to occur more frequently(e.g., every few seconds) to make it harder to exploit.



**Deriverse:** Acknowledged; we think that extracting profit from this approach is unlikely and very expensive.
