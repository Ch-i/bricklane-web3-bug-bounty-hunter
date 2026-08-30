---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Staking amount in QI should be calculated differently
vuln_class: []
---

# Staking amount in QI should be calculated differently

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** Currently, if the stake token is `QI`, `stakingAmountInQi` is [calculated](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L542-544) as shown below:

```solidity
stakingAmountInQi = totalRequiredToken - convertAvaxToToken(token, hostingFee);
```

However, this can result in a precision loss of 1 wei.

**Proof of Concept:** This was tested using a Forge fixture and logs within the source code.

**Recommended Mitigation:** Consider calculating `stakingAmountInQi` directly based on `avaxStakeAmount`.

**BENQI:** Acknowledged. 1 wei precision loss is fine.

**Cyfrin:** Acknowledged.
