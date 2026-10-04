---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-21T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md
tags:
- firm:codespect
- report:2025-08-21-tokentable-sui
title: '[M-01] The claim(...) and claim_with_fees(\.\.\.\.) functions lack token type
  checks'
vuln_class: []
---

# [M-01] The claim(...) and claim_with_fees(\.\.\.\.) functions lack token type checks

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`fungible_token_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_distributor.move#L47), [`fungible_token_with_fees_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/fungible_token_with_fees_distributor.move#L57)

**Description:**

In the `claim(...)` function, there is no check to verify whether the fee token type provided by the caller matches the type configured in `fee_collector`, allowing the caller to use a self-created worthless token to pay the fee.

```move
public entry fun claim<T, F>(...) {
    //...
    assert!(option::is_some(&fee_collector_addr), E_FEE_COLLECTOR_NOT_SET);
    let base_fee = fee_collector::get_fee(fee_config, distributor_address);
    let expected_amount = base_fee * multiplier;
    assert!(coin::value(&fee_payment) == expected_amount, E_INCORRECT_FEES);
    fee_collector::collect_fee(fee_config, fee_payment, ctx);
}
```

In the `claim_with_fees(...)` function, although the fee token is arbitrarily specified by the `authorized_signer`, the signed data contains only the fee amount and no fee token type, making it impossible to verify whether the token paid by the user matches the `authorized_signer`’s expectation.

```move
// Claim data structure with fees
public struct ClaimDataWithFees has drop {
    claimable_timestamp: u64,
    claimable_amount: u64,
    fees: u64
}
```

**Impact:** Users can evade paying token claim fees to the project team.

**Recommendation:** It is recommended that the `claim(...)` function check whether the fee token provided by the user matches the type configured in `fee_collector`.

For `claim_with_fees(...)`, it is recommended to include the fee token type in the signature fields so that the `claim_with_fees` function can perform the check.

**Status:** Fixed

**Client response:** [355c59dae35234a78a9f00893bb3ab5814875dcf](https://github.com/EthSign/ecdsa-token-distributor-sui/commit/355c59dae35234a78a9f00893bb3ab5814875dcf)
