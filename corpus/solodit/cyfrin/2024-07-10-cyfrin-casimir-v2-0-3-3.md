---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-3-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Unused function `validateWithdrawalCredentials()`
vuln_class: []
---

# Unused function `validateWithdrawalCredentials()`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** The function `validateWithdrawalCredentials()` in CasimirManager is private and isn't called anywhere in the contract.

```solidity
function validateWithdrawalCredentials(address withdrawalAddress, bytes memory withdrawalCredentials) // @audit never used
    private
    pure
{
    bytes memory computedWithdrawalCredentials = abi.encodePacked(bytes1(uint8(1)), bytes11(0), withdrawalAddress);
    if (keccak256(computedWithdrawalCredentials) != keccak256(withdrawalCredentials)) {
        revert InvalidWithdrawalCredentials();
    }
}
```

**Recommended Mitigation:** Consider removing the unused function.

**Casimir:**
Fixed in [d6bd8da](https://github.com/casimirlabs/casimir-contracts/commit/d6bd8dae6e8e2f927f34abc3fdb2db15899ae71b).

**Cyfrin:** Verified.
