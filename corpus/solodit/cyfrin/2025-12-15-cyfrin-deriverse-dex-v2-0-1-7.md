---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-15-cyfrin-deriverse-dex-v2-0-1-7
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
title: Missing Quorum Requirement in Governance Voting
vuln_class: []
---

# Missing Quorum Requirement in Governance Voting

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-15-cyfrin-deriverse-dex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-15-cyfrin-deriverse-dex-v2.0.md)_

---

**Description:** The governance voting system in `finalize_voting()` lacks a quorum requirement, allowing protocol parameters to be changed based on relative vote counts without validating that a minimum percentage of total token supply has participated. This enables a small minority of token holders to control protocol governance decisions, undermining the decentralized nature of the system.


```rust
let decr = community_account_header.voting_decr;
let incr = community_account_header.voting_incr;
let unchange = community_account_header.voting_unchange;
let tag = community_account_header.voting_counter % 6;

if decr > unchange && decr > incr {
    // Apply DECREMENT - no quorum check
    match tag {
        0 => { community_account_header.spot_fee_rate -= 1; }
        // ... other parameters
    }
} else if incr > unchange && incr > decr {
    // Apply INCREMENT - no quorum check
    match tag {
        0 => { community_account_header.spot_fee_rate += 1; }
        // ... other parameters
    }
}
```

While `voting_supply` is tracked and set to `drvs_tokens` (total supply), it is never used to validate that sufficient tokens participated in the vote:

```rust
community_account_header.voting_supply = community_account_header.drvs_tokens;
```


**The Problem:**
1. No minimum participation threshold (quorum) is checked before applying voting results
2. A single voter with a small amount of tokens can determine protocol changes if no one else votes
3. The total voting power (`decr + incr + unchange`) is never compared against `voting_supply` or any minimum threshold
4. This violates common governance best practices where significant decisions require meaningful community participation

**Impact:**
- **Governance Attack Vector:** Malicious actors can wait for low-activity periods to push through unfavorable parameter changes
- **Undermined Decentralization:** The voting system fails to ensure decisions represent a meaningful portion of the community

**Recommended Mitigation:** Add a quorum requirement that validates minimum participation before applying voting results. The quorum should be a percentage of the total voting supply.
```rust
        let total_votes = decr + incr + unchange;
        let voting_supply = community_account_header.voting_supply;

        // Add quorum check (e.g., require at least 5% participation)
        const MIN_QUORUM_PERCENTAGE: i64 = 5; // 5% of voting supply
        let min_quorum = (voting_supply * MIN_QUORUM_PERCENTAGE) / 100;
```

**deriverse:**
Fixed in commit [b4e1045](https://github.com/deriverse/protocol-v1/commit/b4e10453eb5fe7a0866a264fac4187167640f998).

**Cyfrin:** Verified.
