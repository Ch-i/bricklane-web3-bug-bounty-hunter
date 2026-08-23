---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-23-cyfrin-sherpa-v2-0-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-11-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-23-cyfrin-sherpa-v2-0
title: Withdrawals can effectively only happen on the primary chain after any yield
  has accrued
vuln_class: []
---

# Withdrawals can effectively only happen on the primary chain after any yield has accrued

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-23-cyfrin-sherpa-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-23-cyfrin-sherpa-v2.0.md)_

---

**Description:** During round rolls, yield is only realized on the primary chain in `SherpaVault::_adjustBalanceAndEmit`. This leaves the system in a problematic state if withdrawals happens on another chain.

Imagine the scenario: there's 500 + 500 deposits of SherpaUSD on chain A and B, A being primary. 100 SherpaUSD is added as yield on A. The balance is 500 + 600, global total 1100 giving a share price of 1.1.
Alice, who has half the total shares decides do withdraw on chain B, giving her 550 SherpaUSD (USDC). Since this isn't available on chain B, the protocol needs to rebalance 50 SherpaUSD from A to B.

They do this by calling `SherpaUSD::ownerBurn(50)` on chain A followed by `SherpaUSD::ownerMint(50)` on chain B. This will store 50 in both `approvedTotalStakedAdjustment` and `approvedAccountingAdjustment` on both chains. The latter one being the issue.

Once `SherpaVault::adjustTotalStaked` is called by the operator, the rebalance of SherpaUSD is done, and Alice can effectively withdraw. However, there's no way to clear the state in `approvedAccountingAdjustment` as no shares were ever moved. If `SherpaVault::adjustAccountingSupply` is called, it will corrupt the `accountingSupply` as no shares were ever moved. So the states of `approvedAccountingAdjustment` are effectively permanently corrupted as `consumeAccountingApproval` can only be cleared from the vault.

In addition to this, if `SherpaVault::adjustAccountingSupply` was called on chain A, `accountingSupply` would be decremented and the `accountingSupply` subtraction in function `_unstake()` would underflow on chain A, hence bricking funds.


**Impact:** Withdrawals can only safely happen on the primary chain as soon as any yield is accrued. If yield is withdraw from the secondary chain that will corrupt either `SherpaUSD.approvedAccountingAdjustment` or `SherpaVault.accountingSupply` on both chains.

**Recommended Mitigation:** Consider split approval modes. Introduce explicit asset-only rebalancing (set `approvedTotalStakedAdjustment` without setting `approvedAccountingAdjustment`) and a share-sync mode (set both).

**Sherpa:** Fixed in commit [`34f2092`](https://github.com/hedgemonyxyz/sherpa-vault-smartcontracts/commit/34f2092f8f882005304c8f1a2ad311ed91d9161a)

**Cyfrin:** Verified. Calls to rebalance assets only were added.

\clearpage
