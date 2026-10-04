---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-08-21-tokentable-sui-1-1
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
title: '[M-02] Distributor has not been assigned a fee collection type'
vuln_class: []
---

# [M-02] Distributor has not been assigned a fee collection type

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-08-21-TokenTable-Sui.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-08-21-TokenTable-Sui.md)_

---

**Files:** [`base_distributor.move`](https://github.com/EthSign/ecdsa-token-distributor-sui/tree/5536d80395d269b7d3392b20a924cbcae7a86344/sources/base_distributor.move#L17)

**Description:**

The current system has two fee collection methods: one is managed by `OwnerCap` through `fee_collector`, which configures the fee token and fee amount; the other allows the `authorized_signer` in each `Distributor` object to arbitrarily specify it in the signed data.

```move
public entry fun claim<T, F>(...) {
    //...
}

public entry fun claim_with_fees<T, F>(...) {
    //...
}
```

However, the `Distributor` object does not have a field distinguishing the fee collection method. As a result, the `authorized_signer` can choose either method or mix them at will.

**Impact:** This causes fee collection to be outside the control of the project team and allows the token issuer to specify it arbitrarily. The project team may suffer losses from the fees.

**Recommendation:** It is recommended to add a field in the `Distributor` to distinguish the fee collection type.

**Status:** Acknowledged

**Client response:** Since fee value will be baked into the signature for claim type `claim_with_fee`, mixed up usaged will cause claim to fail. So there is no risk of fee loss.

**CODESPECT fix review:** The issue in the report is not that users can freely use signatures from the `authorized_signer`—because mixed-up usage would cause the claim to fail—but rather that the `authorized_signer` (controlled by the token distributor) can arbitrarily assign signature types. For example, the project team may want a certain distributor to use the fees configured in `fee_collector`, but the `authorized_signer` could choose to distribute some signatures related to `ungible_token_with_fees_distributor` with a fee of 0, allowing their users to avoid paying fees to the project team. If the project team is willing to accept this, the issue will be marked as acknowledged.

**Client response:** The claim process will be handled by our front-end which will call the right claim type. We will also communicate with `authorized_signer` (the token distributor) in advance to make sure the correctness of signature.
