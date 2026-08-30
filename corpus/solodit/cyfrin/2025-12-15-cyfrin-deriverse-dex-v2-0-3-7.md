---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Insufficient Self-Referral Protection Still Allows Multiple Account Self-Referral
vuln_class: []
---

# Insufficient Self-Referral Protection Still Allows Multiple Account Self-Referral

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The referral validation in the `deposit()` function only prevents self-referral by checking if the referral account address matches the client's account address. However, this allows users to create multiple accounts (with different wallets they control) and self-refer through different accounts.

```rust
if *ref_acc.key == *client_primary_acc.key {
    bail!(InvalidRefAddress {
        expected_address: *client_primary_acc.key,
        actual_address: *ref_acc.key,
    });
}
```

Scenario:
1. User controls `wallet1` and `wallet2`
2. User creates `account A` with `wallet1` and generates referral link
3. User creates `account B` with `wallet2`
4. User uses account A's referral link when depositing with account B (wallet2)
5. User successfully self-refers through different wallets

**Impact:** The referral program's intended purpose of user acquisition is undermined.

**Recommended Mitigation:** Preventing multi-wallet self-referral (where users control multiple wallets) is a fundamental blockchain limitation that may require off-chain solutions like KYC or centralized activities which may not be applicable here.

**Deriverse:** Acknowledged.
