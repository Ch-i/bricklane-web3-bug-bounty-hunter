---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-1-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-02-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md
tags:
- firm:zokyo
- report:2024-02-27-interplanetary-consensus-ipc
title: Deletion Should Be Done After Reading Validator Addresses
vuln_class: []
---

# Deletion Should Be Done After Reading Validator Addresses

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-02-27-InterPlanetary Consensus (IPC).md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary%20Consensus%20%28IPC%29.md)_

---

**Severity** - Medium

**Status** - Resolved

In the function `pruneQuorums()` (L133 LibQuorum.sol) `self.quorumSignatureSenders[h];` is deleted at L143 , then at L145 `values()` are read from the same `self.quorumSignatureSenders[h]` which has been deleted previously , therefore , reading empty values.

**Recommendation**: 

Make the deletion after reading values from `self.quorumSignatureSenders[h];`
