---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: '`onTokenTransfer` does not validate if the call is from the DATA token contract'
vuln_class: []
---

# `onTokenTransfer` does not validate if the call is from the DATA token contract

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

**Severity:** Medium

**Description:** `SponsorshipFactory::onTokenTransfer` and `OperatorFactory::onTokenTransfer` are used to handle the token transfer and contract deployment in a single transaction. But there is no validation that the call is from the DATA token contract and anyone can call these functions.

The impact is low for `Sponsorship` deployment, but for `Operator` deployment, `ClonesUpgradeable.cloneDeterministic` is used with a salt based on the operator token name and the operator address. An attacker can abuse this to cause DoS for deployment.

We see that this validation is implemented correctly in other contracts like `Operator`.
```solidity
       if (msg.sender != address(token)) {
           revert AccessDeniedDATATokenOnly();
       }
```

**Impact:** Attackers can prevent the deployment of `Operator` contracts.

**Recommended Mitigation:** Add a validation to ensure the caller is the actual DATA contract.

**Client:** Fixed in commit [8b13df4](https://github.com/streamr-dev/network-contracts/commit/8b13df49900c640df51e22f7c5a78fcad761f7cb).

**Cyfrin:** Verified.
