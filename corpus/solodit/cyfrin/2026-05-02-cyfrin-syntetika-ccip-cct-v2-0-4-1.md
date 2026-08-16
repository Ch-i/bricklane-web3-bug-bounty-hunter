---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-4-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Use `calldata` instead of `memory` for external function string parameters
vuln_class: []
---

# Use `calldata` instead of `memory` for external function string parameters

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Several external/public functions take `string memory` parameters that are only read, not modified. Changing to `calldata` avoids an unnecessary memory copy.

```solidity
issuance/src/vault/StakingVault.sol
211:        string memory referral
240:        string memory referral
254:        string memory referral
267:        string memory referral
```

**Recommended Mitigation:** For external `stake` and external `mint(shares, referral)`, change `string memory referral` to `string calldata referral`. The public deposit/mint overloads called internally through `stake` must remain memory - verify call graph before applying.

**Syntetika:** Fixed in commit [`ac01ad9`](https://github.com/SyntetikaLabs/monorepo/commit/ac01ad92d7c89285bec898067d03caecf04e3657)

**Cyfrin:** Verified.


\clearpage
