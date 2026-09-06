---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Use `msg.sender` instead of accessing `comptroller` state variable to save
  gas
vuln_class: []
---

# Use `msg.sender` instead of accessing `comptroller` state variable to save gas

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Event `SetTradeFee` in `SablierEscrow` should use `msg.sender` (`CALLER` opcode = 2 gas) instead of accessing the comptroller storage variable (`SLOAD` opcode = 100 gas) to save gas. Since the function can only be called by the `comptroller`, using `msg.sender` is safe.

```solidity
function setTradeFee(UD60x18 newTradeFee) external override onlyComptroller {

        ... ... ...

        // Log the event.
        emit SetTradeFee(address(comptroller), previousTradeFee, newTradeFee);
    }
```

**Recommended Mitigation:** Use `msg.sender` in the event emission instead.

**Sablier:** Fixed in commit [c94cb23](https://github.com/sablier-labs/lockup/commit/c94cb232b62c188e2a1b23ab625bfd5374b92d7a#diff-ba86d209aeed90bf0447759321f08154ad7e0f4edc85849136cba83e27281fbbR162-R280).

**Cyfrin:** Verified.

\clearpage
