---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-2-7
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Aggregated deposit claims can exceed DS Token compliance limits
vuln_class: []
---

# Aggregated deposit claims can exceed DS Token compliance limits

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** `AsyncFundVault::requestDeposit` does not check whether the resulting DS Tokens can be issued to the receiver. After fulfillment, `AsyncFundVault::deposit` and `AsyncFundVault::mint` aggregate all claimable generations and issue the full amount in one call:

```solidity
$.dsToken.issueTokens(receiver, claimedShares);
```

DS Token compliance can reject issuance when:

```text
receiver balance + claimed shares ≥ maximum holdings
```

This can occur because multiple claims are aggregated or because a positive rebase increases the receiver’s balance after the request. The vault does not support partial claims, and fulfilled deposits cannot be cancelled.

**Impact:** The claim may remain blocked until the receiver reduces their balance, another compliant receiver is selected, or an administrator intervenes. If the aggregate amount exceeds the limit for every ordinary receiver, it cannot be claimed through the normal flow.

**Recommended Mitigation:** Support partial claims or split fulfilled entitlements into compliant amounts. Provide a refund or administrative recovery path for fulfilled deposits that cannot pass issuance compliance.

**Securitize:** Acknowledged; this fund does not configure maximum or minimum holdings limits.
