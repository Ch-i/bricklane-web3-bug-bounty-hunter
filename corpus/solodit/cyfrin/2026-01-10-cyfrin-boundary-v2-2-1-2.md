---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Delegate cannot remove delegation issued by a benefactor
vuln_class: []
---

# Delegate cannot remove delegation issued by a benefactor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** A delegate cannot remove delegation issued by a benefactor. Once delegation has been accepted by calling the `acceptDelegatedSigner` function, it can only be revoked by the benefactor by calling the `removeDelegatedSigner` function.

This contradicts the documentation, which states in the `05-Mint-and-Redeem` file that both roles can revoke delegation. Thus, this is a lack of functionality for the delegate.

```
Delegated Signing - Both EOA and contract benefactors can delegate signing to an approved EOA. Delegation requires two steps: benefactor calls initiateDelegatedSigner, delegate calls acceptDelegatedSigner. Either party can remove the delegation.
```
**Recommended Mitigation:** Add functionality to remove delegation for delegate

**Boundary:**
Resolved. Documentation corrected in [PR#165](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/165) - contract behavior is correct, benefactors manage their delegates.

**Cyfrin:** Verified.
