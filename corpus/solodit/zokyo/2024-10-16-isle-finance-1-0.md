---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Reentrancy Vulnerability in the createReceivable Function Allowing Multiple
  Asset Minting
vuln_class: []
---

# Reentrancy Vulnerability in the createReceivable Function Allowing Multiple Asset Minting

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Location**: Receivable.sol

**Description**: 

The createReceivable function in the Receivable contract is vulnerable to reentrancy attacks. This vulnerability arises when the _safeMint function is called, leading to the potential for reentrancy exploits where the minting event can execute multiple times, causing inconsistency between the actual state and emitted events.

**Recommendation**: 

To mitigate the reentrancy vulnerability, it is recommended to use a reentrancy guard to prevent the _safeMint function from being invoked multiple times within the same transaction.

**Client comment**:  

This is a valid operation; however, the seller can mint multiple receivables through Receivable::createReceivable by default. Although multiple receivables are created, they must still be approved by the Pool Admin before proceeding with the LoanManager::requestLoan operation. We are uncertain about the potential impact of minting a large number of receivables at once. While re-entrancy can occur during minting, the event emission remains consistent and in the correct order.

**Suggested action**: 

Go back through the code and absolutely assert and triple check that free minting receivables doesn't have any impact to the protocol
