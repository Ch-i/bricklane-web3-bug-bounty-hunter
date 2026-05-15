---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-parcel-payroll-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-parcel-payroll
title: '[L-01] EIP-712 domain separator is not implemented correctly'
vuln_class: []
---

# [L-01] EIP-712 domain separator is not implemented correctly

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-Parcel Payroll.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-Parcel%20Payroll.md)_

---

The domain separator in `Signature` is missing the `name`, `version` and `salt` fields defined in EIP-712. The standard states that not all fields are mandatory but adding them would add another layer of security for the usage of off-chain signed messages for the protocol. Refer to the [EIP712 doc](https://eips.ethereum.org/EIPS/eip-712) and add all of the missing domain separator fields.
