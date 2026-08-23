---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-wrappedelon-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-wrappedelon
title: '[M-01] Centralization attack vector is present in `setEnabledState`'
vuln_class: []
---

# [M-01] Centralization attack vector is present in `setEnabledState`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-WrappedElon.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md)_

---

**Severity**

**Impact:**
High, as an owner can block unwrapping of wrapped assets

**Likelihood:**
Low, as it requires a malicious or a compromised owner

**Description**

The `setEnabledState` method of `WrappedElon` allows the owner of the contract to disable (or enable) wrapping and unwrapping of tokens. The issue is that a malicious or a compromised owner can decide to act in a bad way towards users and block unwrapping of the tokens, essentially locking them out of their funds. If the ownership is burned then (or private keys are lost) it will be irreversible.

**Recommendations**

Potential mitigations here are to use governance or a multi-sig as the contract owner. Even better is to use a Timelock contract that allows users to be notified prior to enabling/disabling wrapping/unwrapping so that they can take action, although this removes the benefit of using the method as a risk mitigation for bridge attacks.
