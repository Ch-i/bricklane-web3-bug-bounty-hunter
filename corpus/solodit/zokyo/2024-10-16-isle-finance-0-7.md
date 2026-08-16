---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: NFT Holder Cannot Withdraw Repaid Amount Due to Loan Seller Check
vuln_class: []
---

# NFT Holder Cannot Withdraw Repaid Amount Due to Loan Seller Check

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Location** LoanManager.sol, Receivable.sol

**Description**: 

The Receivable NFT, which represents a transferable debt claim, restricts the ability to withdraw the repayment of the debt to the original lender (loan_.seller) while allowing the transfer of the NFT. In the LoanManager.sol contract, the withdrawFunds() function checks if the caller is the original lender, preventing new NFT holders from accessing repaid funds. This disallows the transfer of the debt along with its claim, leading to potential disputes and misrepresentations in transactions involving the NFT.

**Recommendation** 

Since that the debt is meant to be claimed by the original lender, it would be consistent to have non-transferrable Receivable NFT. This change will ensure that the current owner of the Receivable NFT can rightfully claim the repayment of the debt.

**Client comment#1** : The amount that can be withdrawn is not the repaid amount, it is the early payment amount from Isle’s pool. Right now we fix this issue through a removed seller address check in the withdrawalFunds(), we let the holder of NFT have the right to withdraw.
