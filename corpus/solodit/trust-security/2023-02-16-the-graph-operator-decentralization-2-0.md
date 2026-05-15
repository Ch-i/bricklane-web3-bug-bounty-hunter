---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-02-16-the-graph-operator-decentralization-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-02-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md
tags:
- firm:trust-security
- report:2023-02-16-the-graph-operator-decentralization
title: Improve documentation
vuln_class: []
---

# Improve documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Trust Security_  
_Source report: [2023-02-16-The Graph Operator Decentralization.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-02-16-The%20Graph%20Operator%20Decentralization.md)_

---

Documentation of the `collect()` function states:
```solidity
        /**
            * @dev Collect query fees from state channels and assign them to an allocation.
            * Funds received are only accepted from a valid sender.
            * To avoid reverting on the withdrawal from channel flow this 
         function will:
             * 1) Accept calls with zero tokens.
             * 2) Accept calls after an allocation passed the dispute period, in that case, all
                * the received tokens are burned.
                * @param _tokens Amount of tokens to collect
                * @param _allocationID Allocation where the tokens will be assigned
                */
```
Note that the highlighted text is no longer relevant, now that the operator is decentralized. 
It should be omitted.
