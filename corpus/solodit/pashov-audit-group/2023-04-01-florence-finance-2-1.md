---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-02] The ERC4626 standard is not followed correctly'
vuln_class: []
---

# [M-02] The ERC4626 standard is not followed correctly

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
Medium, as functionality is not working as expected but without a value loss

**Likelihood:**
Medium, as multiple methods are not compliant with the standard

**Description**

As per EIP-4626, the `maxDeposit` method "MUST factor in both global and user-specific limits, like if deposits are entirely disabled (even temporarily) it MUST return 0.". This is not the case currently, as even if the contract is paused, the `maxDeposit` method will still return what it usually does.

When it comes to the `decimals` method, the EIP says: "Although the convertTo functions should eliminate the need for any use of an EIP-4626 Vault’s decimals variable, it is still strongly recommended to mirror the underlying token’s decimals if at all possible, to eliminate possible sources of confusion and simplify integration across front-ends and for other off-chain users."
The `LoanVault` contract has hardcoded the value of 18 to be returned when `decimals` are called, but it should be the decimals of the underlying token (it might not be 18 in some case maybe).

**Recommendations**

Go through [the standard](https://eips.ethereum.org/EIPS/eip-4626) and follow it for all methods that `override` methods from the inherited ERC4626 implementation.
