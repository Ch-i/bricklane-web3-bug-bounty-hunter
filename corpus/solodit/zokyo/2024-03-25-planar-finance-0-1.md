---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-0-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Potential Gas Limit Issues in Contract Functions Due to High Number of User
  Positions
vuln_class: []
---

# Potential Gas Limit Issues in Contract Functions Due to High Number of User Positions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Medium

**Status**:  Acknowledged 

**Description**:

The `LpNFTpool` contains several functions (`mergePositions`, `harvestAllPositions`, `withdrawFromAllPositions`, etc.) that iterate over user's staking positions or token IDs. In scenarios where a user has a large number of positions or tokens, these functions are prone to hitting the block gas limit, resulting in transactions that fail to execute. This not only hinders the user's ability to interact with the contract as intended but also may lead to situations where users are unable to consolidate, harvest, or withdraw from their positions without resorting to less efficient methods.

**Scenario:**

Consider a user who, over time, has accumulated a significantly large number of staking positions or NFTs within the system. If this user attempts to use a function like `mergePositions` to consolidate these positions into one or `harvestAllPositions` to claim rewards across all positions, the transaction could require an amount of gas that exceeds the block gas limit, making it impossible to execute the transaction successfully. This scenario can lead to frustration for users and could potentially lock users out of their assets or rewards under certain conditions.

**Recommendations:**

Implement Batch Processing: Consider adding functionality that allows users to specify subsets of positions or tokens for processing within a single transaction. By operating on smaller batches, users can avoid the gas limit issue while still being able to perform the desired actions on all their positions over several transactions.

**Note#3**: We don't have `harvestAllPositions` or `withdrawFromAllPositions` in LpNFT Pool contract. We shall leave `mergePositions` as it is and maybe consider batch processing mergers on frontend.
