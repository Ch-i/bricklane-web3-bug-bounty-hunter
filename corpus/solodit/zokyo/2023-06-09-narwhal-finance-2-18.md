---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-18
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Missing Validation Zero address validation
vuln_class: []
---

# Missing Validation Zero address validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity** : Low

**Status**: Resolved

**Description**:

The setManager function in the PairInfos contract allows the gov address to set a new manager address. However, this function does not include a check to ensure that the new manager address is not a zero address. This can lead to unexpected behavior or unintended consequences.


If the manager address is set to the zero address, it can cause issues with the functionality of the contract. For example, if the manager address is used to interact with external contracts or services, then the contract may fail to interact properly or lose access to critical functionality if the manager address is set to zero. Additionally, if the manager address is used to control access to the contract, then setting the address to zero could potentially allow unauthorized users to interact with the contract.

**Recommendation**:

To mitigate this vulnerability, a check should be added to the setManager function to ensure that the new manager address is not a zero address. This can be accomplished by adding an if statement that checks if the new address is zero, and if so, reverts the transaction.

**Fixed**: Issue fixed in commit a72e06b
