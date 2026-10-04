---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-07-02-hyperwave-sub-account-strategy-framework-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-07-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md
tags:
- firm:codespect
- report:2026-07-02-hyperwave-sub-account-strategy-framework
title: '[I-01] transferFundBackToVault(...) floors allocated to zero while transferring
  the full amount'
vuln_class: []
---

# [I-01] transferFundBackToVault(...) floors allocated to zero while transferring the full amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-07-02-Hyperwave-Sub-Account-Strategy-Framework.md)_

---

**Files:** [SubAccountFundManager.sol](https://github.com/SwellNetwork/boring-vault/blob/6f6cd157b9aa4f63263e70339bbc37106cede493/src/base/Roles/SubAccountFundManager.sol)

**Description:**

`transferFundBackToVault(amount)` sets `allocated[msg.sender]` to `0` when `amount > allocated[msg.sender]`, but still calls `baseAsset.safeTransferFrom(msg.sender, address(boringVault), amount)` for the full amount. `allocated[msg.sender]` is only increased in `transferFundFromVault` when tokens leave the vault, so it never exceeds the strategy’s actual debt and cannot be driven below it.

**Impact:** A strategy that returns more than it owes transfers the excess (`amount - allocated[msg.sender]`) into the vault while `allocated` is set to `0`, leaving the excess untracked.

**Recommendation:** Cap the decrease and the transfer to `allocated[msg.sender]`, or revert when `amount > allocated[msg.sender]`.

**Status:** Acknowledged

**Client response:** It is intended. After pulling fund from the vault and running strategy, sub account gets yield and repay amount can be greater than pulling amount

**CODESPECT fix review:** Acknowledged.
