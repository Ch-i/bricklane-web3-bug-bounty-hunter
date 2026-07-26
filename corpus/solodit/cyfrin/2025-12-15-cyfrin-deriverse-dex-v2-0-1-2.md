---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Accounts may be created with incorrect rent-exemption due to `Rent::default`
  usage
vuln_class: []
---

# Accounts may be created with incorrect rent-exemption due to `Rent::default` usage

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** This dos vulnerability arises from the use of hardcoded `rent` parameters during account creation, leading to underfunded accounts that fail rent exemption requirements.

The flawed implementation relies on `Rent::default` instead of the on-chain `Rent sysvar` for rent calculations, creating accounts with insufficient funds for rent exemption.

```rust
    let rent = &Rent::default();
    ...
    let spl_lamports: u64 = rent.minimum_balance(165);

```

The implementation never reads the on-chain Rent `sysvar` (e.g., `Rent::get` or passing the rent `sysvar` account), so the computed minimum balances may not reflect the cluster’s actual rent parameters.


**Impact:** As a result, accounts can be created non–rent-exempt, causing DOS.

**Recommended Mitigation:** It is recommended to use `Rent::get` instead of `Rent::default`.

**Deriverse:** Fixed in commit [d319206](https://github.com/deriverse/protocol-v1/commit/d319206f269efdd6ba1de8ae5966e02f9ffcfec7).

**Cyfrin:** Verified.
