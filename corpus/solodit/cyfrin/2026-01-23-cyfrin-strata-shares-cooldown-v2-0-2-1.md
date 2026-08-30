---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-23-cyfrin-strata-shares-cooldown-v2-0-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-23-cyfrin-strata-shares-cooldown-v2-0
title: SharesCooldown Does Not Enforce Spec-Defined Pause Lockup Rules
vuln_class: []
---

# SharesCooldown Does Not Enforce Spec-Defined Pause Lockup Rules

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-23-cyfrin-strata-shares-cooldown-v2.0.md)_

---

**Description:** The spec (SIP-01 §7) requires that when redemptions are paused:

- Finalization must revert

- Locked shares must remain held in the Silo

However, cancel() allows users to bypass this by retrieving their shares even during a global pause:

```solidity
    function cancel(IERC20 vault, address user, uint256 i) external onlyUser(user) {

        TRequest[] storage requests = activeRequests[address(vault)][user];
        uint256 len = requests.length;
        require(i < len, "OutOfRange");
        TRequest memory req = requests[i];
        if (i < len - 1) {
            requests[i] = requests[len - 1];
        }
        requests.pop();
        vault.transfer(user, req.shares); // @note берет ли cancel комиссии?
        emit RequestCanceled(address(vault), user, req.shares);
    }
```

**Remediation:**
Update the specification to reflect that cancellation are always allowed and pauses do not fully lock shares.

**Strata:** SIP updated here: [69f3eb58](https://github.com/Strata-Money/contracts-tranches/commit/69f3eb58696c44bd9e2c9890ec9023ebc9d1722e)

**Cyfrin:** Verified.
