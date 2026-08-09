---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Incorrectly named return variable `AutoRedemption::calculateUSDsToTargetPrice`
vuln_class: []
---

# Incorrectly named return variable `AutoRedemption::calculateUSDsToTargetPrice`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** `AutoRedemption::calculateUSDsToTargetPrice` has the following signature:

```solidity
function calculateUSDsToTargetPrice() private view returns (uint256 _usdc)
```

However, the named return variable is semantically incorrect and should instead be `_usds` to avoid confusion.

**The Standard DAO:** Fixed by commit [a03f0d5](https://github.com/the-standard/smart-vault/commit/a03f0d54637195d34ed17f9a7540d6f201eef55d).

**Cyfrin:** Verified. The return variable has been renamed.
