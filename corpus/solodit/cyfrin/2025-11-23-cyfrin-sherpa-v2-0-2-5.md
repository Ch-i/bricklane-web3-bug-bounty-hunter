---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-2-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Consider implementing explicit rounding behaviour instead of default round
  down
vuln_class: []
---

# Consider implementing explicit rounding behaviour instead of default round down

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** All functions in `ShareMath.sol` round down to the nearest integer currently. This can be unfavourable in certain instances for the SherpaVault.

For example, the `ShareMath.pricePerShare` function uses integer division which causes precision loss. Hence it would slightly underestimate the price per share.

```solidity
function pricePerShare(
    uint256 totalSupply,
    uint256 totalBalance,
    uint256 pendingAmount,
    uint256 decimals
) internal pure returns (uint256) {
    uint256 singleShare = 10 ** decimals;
    return
        totalSupply > 0
            ? (singleShare * (totalBalance - pendingAmount)) / totalSupply
            : singleShare;
}
```

**Recommended Mitigation:** It is recommend to perform explicit rounding in addition to adding comments that logically elaborate why the respective rounding direction is appropriate in each instance.

**Sherpa:** Fixed in commit [`61345a1`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/61345a1967311167ec8fe4dba81bb2a21247ea50)

**Cyfrin:** Verified. Documentation about the specific rounding directions added.

\clearpage
