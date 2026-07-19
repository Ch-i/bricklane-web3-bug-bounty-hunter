---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-3-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Incomplete Balance Check Missing Transaction Fee and Reserve Balance
vuln_class: []
---

# Incomplete Balance Check Missing Transaction Fee and Reserve Balance

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `create_client_account()` function checks if the wallet has sufficient balance to create two accounts, but it does not account for transaction fees or reserve balance for the wallet itself. This can lead to transaction failures or leave the wallet account in an unusable state after the operation.

When creating client accounts, the code only verifies that the wallet balance covers the rent-exempt minimums for the two new accounts:
```rust
    if balance < client_primary_lamports + client_community_lamports {
        bail!(InsufficientFunds);
    }
```

After the two `create_account` instructions execute, the wallet transfers:
- `client_primary_lamports` to the primary account
- `client_community_lamports` to the community account

If the wallet's initial balance was exactly `client_primary_lamports + client_community_lamports`, the wallet would be left with:
- 0 lamports (or very close to 0)
- Unable to pay transaction fees
- Potentially unable to perform subsequent operations


**Impact:** If a wallet has exactly `client_primary_lamports + client_community_lamports` balance, the transaction may fail during execution.

**Recommended Mitigation:** Reserve a small, predefined amount (e.g., a few thousand lamports) on top of the required rent-exempt minimums.
```rust
const WALLET_RESERVE_LAMPORTS: u64 = 5_000_000; // example reserve
if balance < client_primary_lamports + client_community_lamports + WALLET_RESERVE_LAMPORTS {
    bail!(InsufficientFunds);
}
```

**Deriverse:** Fixed in commit [548040f](https://github.com/deriverse/protocol-v1/commit/548040fcce8e00f6b42546a19e79a4bd7d0fb5d0).

**Cyfrin:** Verified.
