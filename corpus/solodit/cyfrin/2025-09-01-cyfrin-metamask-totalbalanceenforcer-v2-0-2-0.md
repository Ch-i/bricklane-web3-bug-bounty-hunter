---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-2-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0
title: Insufficient documentation of "TotalBalanceChangeEnforcer" can lead to incorrect
  use of enforcers
vuln_class: []
---

# Insufficient documentation of "TotalBalanceChangeEnforcer" can lead to incorrect use of enforcers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md)_

---

**Description:** The current documentation for Total Balance Change Enforcers is misleading and lacks clear guidance on when to use each enforcer type. This confusion may lead developers to incorrectly use `TotalBalanceChangeEnforcer` for independent security constraints instead of `BalanceChangeEnforcer`, resulting in weakened security through incorrect constrains.

The documentation fails to clearly distinguish between two fundamentally different use cases:

_Independent security constraints_ -  multiple delegations each imposing limits
_Coordinated multi-operation transactions_ single complex transaction with multiple steps

Current documentation provides following example without sufficient context

```text
Consider a delegation chain with 3 instances of ERC20TotalBalanceChangeEnforcer:

Enforcer 1: Expects an increase of at least 1000 tokens
Enforcer 2: Expects an increase of at least 200 tokens
Enforcer 3: Expects a decrease of at most 300 tokens

Accumulate expected changes: +1000 + 200 - 300 = +900
Validate that the final balance has increased by at least 900 tokens

```
The documentation doesn't explain:

- Why accumulation is appropriate here vs. taking the most restrictive constraint
- When this pattern should be used
- What happens to individual enforcer requirements (Enforcer 1's ≥1000 requirement)

Current documentation lacks guidance for developers to choose between enforcer types, leading to incorrect usage patterns.

Another important insight missing is the fact that `TotalBalanceChangeEnforcer` class of caveats can persist state across multiple executions in a batched execution environment. Since the `hashkey` does not include delegation hash, the same `TotalBalanceChangeEnforcer` can share state across multiple, unrelated execution call datas, as long as the token and recipient are the same.



**Impact:** Developers using wrong enforcer type leading to constraint violations and security bypasses.

For example, if developer intent is to create progressively stricter delegation chain:

```text
Alice delegates to Bob: "Treasury can lose max 100 ETH"
Bob delegates to Dave: "Treasury can lose max 50 ETH" (more restrictive)
Expected behavior: Enforce 50 ETH limit (stricter wins)

Using TotalBalanceChangeEnforcer:
Alice: TotalBalanceChangeEnforcer (expectedDecrease = 100 ETH)
Bob: TotalBalanceChangeEnforcer (expectedDecrease = 50 ETH)
Accumulation: 100 + 50 = 150 ETH total decrease allowed
```

In the above example, delegation chain becomes MORE permissive instead of more restrictive.


**Recommended Mitigation:** Consider:

1. Consider updating documentation top provide clear context to developers on when to use total balance change enforcer v/s balance change enforcer
2. Consider adding documentation that clearly specifies that multiple executions in a `batch execution` environment can use the same instance of `TotalBalanceChangeEnforcer` contracts and hence share state of total balances
3. Consider renaming `TotalBalanceChangeEnforcer` to `MultiOperationBalanceEnforcer` for better clarity

**Metamask:** Fixed in [PR 144](https://github.com/MetaMask/delegation-framework/pull/144/commits/7e680b27e29aaa1caaacd33286d1346376cab3c3)

**Cyfrin:** Verified.
