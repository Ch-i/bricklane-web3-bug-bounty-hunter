---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Incomplete reward transfer due to balance shortfall
vuln_class: []
---

# Incomplete reward transfer due to balance shortfall

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Medium

**Status**:  Acknowledged 

**Description**

The `_safeRewardsTransfer` function within the `LpNFTPool` contract is designed to transfer reward tokens safely to users, guarding against rounding errors or situations where the contract's token balance is insufficient to cover all pending rewards. However, the current implementation does not account for scenarios where the contract's balance of `planeToken` is lower than the amount intended for transfer. In such cases, the function reduces the transfer amount to the available balance, potentially leaving a portion of the owed rewards unclaimed. This situation can lead to users not receiving the full rewards they are entitled to.

**Recommendation**: 

Consider implementing a mechanism that tracks the shortfall in reward payments. Introduce a mapping to track the leftover rewards for each user. When the transfer amount is adjusted due to a balance shortfall, record the difference between the intended and actual transferred amounts in the user's shortfall record.

**Note#2**: `_safeRewardsTransfer` is an internal function which is called as part of a chain of events in `harvestPosition` or `harvestPositionTo` external functions. These functions call `_updatePool` to update balance of the LpNFT Pool before `_safeRewardsTransfer`. Since technically, the user gets particular percentage of the rewards owed by the LpNFT from the `PlanerMaster` contract, practically, it is not possible for the LpNFT Pool to have less balance than a user is owing. The capping in `_safeRewardsTransfer` function is merely a safety valve. We're keeping the code as is for this.
