---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-13
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`RevenueLock`: Missing Funding Validation, Can Be Underfunded While Claims
  Remain Enabled'
vuln_class: []
---

# `RevenueLock`: Missing Funding Validation, Can Be Underfunded While Claims Remain Enabled

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `RevenueLock` stores beneficiary allocations and `totalAllocation`, but it does not enforce an on-chain funding check before claims are used.

If the contract holds less than the intended `2,400,000 ARM`, beneficiaries can still appear entitled, but actual payouts depend on the remaining token balance in the contract.

- early beneficiaries may claim successfully
- later beneficiaries may revert once balance is insufficient
- failed claims do not reduce recorded allocation, but they block payout until more ARM is funded

**Impact:** Example:
- total configured allocation = `2,400,000 ARM`
- actual contract balance = `1,200,000 ARM`
- revenue reaches a milestone that unlocks claims

Result:
- some beneficiaries may claim
- later beneficiaries may revert with `RevenueLock: transfer failed`
- the contract becomes unfairly order-dependent under underfunding

**Recommended Mitigation:** Add an on-chain funding/activation check before claims are allowed.

**Armada:** Fixed in commit [c05d5f7](https://github.com/ship-armada/armada-poc/commit/c05d5f7e3bb0fa7a53bf5b49db06e929d527cb27).

**Cyfrin:** Verified.
