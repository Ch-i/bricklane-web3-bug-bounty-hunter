---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-06-01-protectorate-1-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-06-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md
tags:
- firm:pashov-audit-group
- report:2023-06-01-protectorate
title: '[H-01] Vesting schedule for a beneficiary can be overwritten'
vuln_class: []
---

# [H-01] Vesting schedule for a beneficiary can be overwritten

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-06-01-Protectorate.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-06-01-Protectorate.md)_

---

**Impact:**
High, as the amount left to be vested will be stuck in the contract forever

**Likelihood:**
Medium, as it requires more than 1 vesting schedule for the same beneficiary

**Description**

The vesting schedules in `Vesting` are saved in `schedules` mapping, which uses the `_beneficiary` address as the key. The problem is that if a beneficiary has a scheduled vesting already, if a second schedule is set to it, then the first one will be overwritten but the `schedulesTotalAmount` will still hold the first scheduled funds to vest. This means they will be stuck in the `Vesting` contract forever.

**Recommendations**

A possible solution is to use a vesting ID instead of the `beneficiary` address as the key in the `schedules` mapping or to disallow multiple schedules set for the same `beneficiary`.
