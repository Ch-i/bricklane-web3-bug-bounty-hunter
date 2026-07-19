---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-0-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: Fee Discount Calculation Ignores Base Currency Value Differences
vuln_class: []
---

# Fee Discount Calculation Ignores Base Currency Value Differences

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The fee discount calculation in `fees_deposit` uses the raw token amount divided by decimal factor, without considering the actual value differences between base currencies. This can lead to unfair discount distribution when multiple base currencies with different values are supported.

In `fees_deposit`, the `prepayment` amount is calculated as:
```rust
let dec_factor = get_dec_factor(community_state.base_crncy[crncy_index].decs_count) as f64;
let prepayment = data.amount as f64 / dec_factor;
let fees_discount = community_state.fees_discount(prepayment);
```
The calculation only normalizes for decimal places but does not account for the actual value of different base currencies. For example:
- Depositing 1000 USDC (worth $1000)
- Depositing 1000 tokens of a low-value base currency (worth $0.001 each = $1 total)
- Deposit 1000 SOL would be quite impossible

Both would receive the same discount rate, despite a 1000x value difference.

This becomes more problematic as **the protocol expands to support additional base currencies through governance, as mentioned in the documentation. Different base currencies may have vastly different market values, but the current implementation treats them equally based on raw token count.**

From the documentation https://deriverse.gitbook.io/deriverse-v1/launchpad/launchpad#supported-base-currency:

```plaintext
Supported Base Currency
Current Support:

USDC: Circle USD Stablecoin

Future Expansion:

- Additional base currencies may be added through governance

- Multi-denomination support under consideration

- Community can propose new base currencies
```

**Impact:** Unfair discount distribution: Users depositing low-value base currencies can achieve the same discount thresholds as users depositing high-value currencies with much less actual value

**Recommended Mitigation:** Store a value normalization factor for each base currency that represents its relative value.

**Deriverse:** Fixed in commit [35602457](https://github.com/deriverse/protocol-v1/commit/35602457ebebccacca51749aad6270077724fb38).

**Cyfrin:** Verified.
