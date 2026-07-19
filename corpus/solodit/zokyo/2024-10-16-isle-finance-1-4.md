---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-4
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
title: Lack of reentrancy guards where ERC721 is used increases the risk profile for
  reentrancy issues
vuln_class: []
---

# Lack of reentrancy guards where ERC721 is used increases the risk profile for reentrancy issues

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged

**Location**: Receivable.sol#createReceivable,LoanManager.sol#withdrawFunds

**Recommendation**
 
There are various locations in the codebase where an ERC721 token is being transferred or minted; however, there are no reentrancy guards used. It’s recommended that for functions that are interacting with external contracts that support a callback functionality (for instance ERC721.safeMint and ERC721.safeTransferFrom calls upon an onERC721Received callback during a safe transfer) uses a reentrancy guard where recursive programming is not desired to mitigate the risk of undiscovered reentrancy vulnerabilities.
