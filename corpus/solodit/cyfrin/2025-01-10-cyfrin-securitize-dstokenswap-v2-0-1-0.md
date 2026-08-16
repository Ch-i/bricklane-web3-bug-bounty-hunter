---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-01-10-cyfrin-securitize-dstokenswap-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-10-cyfrin-securitize-dstokenswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-01-10-cyfrin-securitize-dstokenswap-v2-0
title: Missing zero address validation in initialize function
vuln_class: []
---

# Missing zero address validation in initialize function

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-01-10-cyfrin-securitize-dstokenswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-10-cyfrin-securitize-dstokenswap-v2.0.md)_

---

**Description:** The `initialize` function in `DSTokenClassSwap` contract does not validate that the input addresses `_sourceDSToken` and `_targetDSToken` are non-zero addresses.

```solidity
DSTokenClassSwap.sol
40:     function initialize(address _sourceDSToken, address _targetDSToken) public override onlyProxy initializer {
41:         __BaseDSContract_init();
42:         sourceDSToken = IDSToken(_sourceDSToken);//@audit-issue INFO check zero address
43:         sourceServiceConsumer = IDSServiceConsumer(_sourceDSToken);
44:         targetDSToken = IDSToken(_targetDSToken);
45:         targetServiceConsumer = IDSServiceConsumer(_targetDSToken);
46:     }
```

**Recommended Mitigation:** Add zero address validation checks.

**Securitize:** Fixed in commit [b26a16](https://bitbucket.org/securitize_dev/bc-dstoken-class-swap-sc/commits/b26a167524dfa96fc92dc18a863998a50e533bf2).

**Cyfrin:** Verified.


\clearpage
