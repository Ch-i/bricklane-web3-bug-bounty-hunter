---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Dynamic LP fees will remain zero by default unless explicitly updated
vuln_class: []
---

# Dynamic LP fees will remain zero by default unless explicitly updated

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** As given by the logic in `LPFeeLibrary::getInitialLPFee`, dynamic fee pools initialize with an LP fee of 0%:

```solidity
function getInitialLPFee(uint24 self) internal pure returns (uint24) {
    // the initial fee for a dynamic fee pool is 0
    if (self.isDynamicFee()) return 0;
    self.validate();
    return self;
}
```

While `AngstromL2::setPoolLPFee` allows the contract owner to update the dynamic LP fee, there will be a period following initialization when it is not set. As such, it may be desirable to implement the `afterInitialize()` hook if a non-zero LP fee is required immediately upon initialization.

**Impact:** The LP fee will remain zero for all pools unless explicitly updated by the hook owner.

**Proof of Concept:** The following test should be added to `AngstromL2.t.sol`:

```solidity
function test_zeroInitialLPFee() public {
    PoolKey memory key = initializePool(address(token), 10, 3);
    assertEq(manager.getSlot0(key.toId()).lpFee(), 0);
}
```

**Recommended Mitigation:** Implement the `afterInitialize()` hook to set the desired LP fee immediately upon initialization.

**Sorella Labs:** Fixed in commit [ffb9fb2](https://github.com/SorellaLabs/l2-angstrom/commit/ffb9fb20e5b0afbf6996ef9528ef10acd8c94f91#diff-eff6e215636c02633f38518bd4bf97879ede5fdd1586aa6d73fc2ab3fa816396).

**Cyfrin:** Verified. Dynamic fee pools are no longer supported.
