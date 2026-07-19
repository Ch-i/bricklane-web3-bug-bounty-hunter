---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-15T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-15-cyfrin-deriverse-dex-v2-0
title: '`ClientCommunityState::update` function does not update the `rate` before
  calculating new `dividends_value`'
vuln_class: []
---

# `ClientCommunityState::update` function does not update the `rate` before calculating new `dividends_value`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The `ClientCommunityState::update` function is responsible for distributing dividends based on the amount of DRVS tokens a user holds:
```rust
for (i, d) in self.data.iter_mut().enumerate() {
    let amount = (((community_state.base_crncy[i].rate - d.dividends_rate)
        * self.header.drvs_tokens as f64) as i64)
        .max(0);
    d.dividends_value += amount;
}
```
The value of `community_state.base_crncy[i].rate` is updated every hour through the dividend allocation function.

However, there is a possibility that more than one hour has passed since the last allocation and dividend allocation function is not called and our current implementation does not update the `rate` in such cases. As a result, the calculation may rely on stale `rate`, and `dividends_value` may be computed using a stale `community_state.base_crncy[i].rate`.

Scenario:
1. One hour has just passed, but the dividend allocation function is not called.
2. The user calls withdraw to withdraw DRVS tokens, which also does not update the rates.
3. As a result, the user receives a lower dividend value because the calculation is based on an outdated rate.

The scenario described above involves the withdraw functionality, but a similar issue can occur with deposit as well:
1. One hour has just passed, but the dividend allocation function is not called.
2. A user purchases DRVS tokens and calls deposit. However, we record the old rate as the user’s `dividends_rate`.
3. The user can then call the dividend allocation function and receive dividends that they should not be entitled to, because they did not hold those DRVS tokens during the previous hour.

**Impact:** If the dividend allocation function is not called before update, and more than one hour has passed, it can result in some users unfairly incurring losses while others receive undeserved profits.

**Recommended Mitigation:** Update `community_state.base_crncy[i].rate` if one hour has passed before updating `dividends_value` and `dividends_rate`.

**Deriverse:** Fixed in commit [ca593e](https://github.com/deriverse/protocol-v1/commit/ca593e2bc30b93a7a4a53c69ceb5b91a282c8955).

**Cyfrin:** Verified.
