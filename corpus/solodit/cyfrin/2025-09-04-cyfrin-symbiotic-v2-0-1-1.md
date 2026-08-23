---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: '`unwhitelistOperator` allows state changes when whitelist Is disabled, causing
  inconsistent operator state'
vuln_class: []
---

# `unwhitelistOperator` allows state changes when whitelist Is disabled, causing inconsistent operator state

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** The `unwhitelistOperator` function performs state changes (removing an operator from the whitelist and potentially unregistering them) even when the whitelist feature is **disabled**. This violates the expected behavior that **whitelist enforcement should only be active when explicitly enabled**.

Unwhitelisting an operator while the whitelist is disabled silently alters the contract’s state. Later, when the whitelist is re-enabled, the operator is unexpectedly no longer whitelisted — even though no whitelist-related logic was supposed to be active when they were removed.

**Impact:** When the whitelist feature is disabled, `unwhitelistOperator` silently processes changes, leading to an inconsistent state. If the whitelist is re-enabled, an operator who was unwhitelisted, remains registered, leading to inconsistent state.

**Recommended Mitigation:** Consider preventing `unwhitelistOperator` from executing when whitelist is disabled. Either revert explicitly or skip execution:

```solidity
function unwhitelistOperator(address operator) public virtual checkPermission {
    if (!isWhitelistEnabled()) {
        revert OperatorsWhitelist_WhitelistDisabled( );
    }

    _getOperatorsWhitelistStorage()._whitelisted[operator] = false;

    if (isOperatorRegistered(operator)) {
        _unregisterOperator(operator);
    }

    emit UnwhitelistOperator(operator);
}
```
**Symbiotic:** Fixed in [32bea5e](https://github.com/symbioticfi/relay-contracts/pull/36/commits/32bea5ee73a1085f68645ef460f8c411c96cfcbe).

**Cyfrin:** Verified.

\clearpage
