---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-bridgex-v2-0-2-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-bridgex-v2-0
title: '`Token::setIssuer` allows setting issuer to `address(0)`, disabling minting'
vuln_class: []
---

# `Token::setIssuer` allows setting issuer to `address(0)`, disabling minting

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-bridgex-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-bridgex-v2.0.md)_

---

**Description:** `Token::constructor` validates that the issuer is non-zero, but `setIssuer` has no such check:

```solidity
// Token.sol:51 — constructor validates
require(tokenIssuer != address(0)); // dev: invalid issuer

// Token.sol:92-98 — setIssuer does not
function setIssuer(address newIssuer)
external
only(owner) {
    issuer = newIssuer; // no zero-address check
    emit NewIssuer(issuer);
}
```

Setting `issuer` to `address(0)` disables minting since `msg.sender` can never equal `address(0)`, and only the owner (not the issuer) can call `setIssuer` to recover. The Certora spec `mintAlwaysRevertsAfterZeroIssuer` in `Token.spec` confirms this behavior.

**Impact:** If the owner accidentally calls `setIssuer` with `address(0)`, minting is permanently disabled. The `PublicBridge::_releaseTokens` mint fallback would also break, forcing all releases to depend entirely on vault balance. This may be intentional to disable minting post-distribution, but the inconsistency with the constructor check suggests an oversight.

**Recommended Mitigation:** If this behavior is not desired, add a zero-address check consistent with the constructor:

```solidity
function setIssuer(address newIssuer) external only(owner) {
    require(newIssuer != address(0)); // dev: invalid issuer
    issuer = newIssuer;
    emit NewIssuer(issuer);
}
```

**BridgeX:**
Fixed in commit [c0c2f38](https://github.com/NerdUnited-NodeGovernance/audit-2026-03-bridgex/commit/c0c2f38eb6731acf2d6ebfca252dcba33a26c0fe).

**Cyfrin:** Verified.
