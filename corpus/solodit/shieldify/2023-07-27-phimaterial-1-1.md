---
affected_contracts: []
derives_from: []
id: solodit-shieldify-2023-07-27-phimaterial-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-07-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md
tags:
- firm:shieldify
- report:2023-07-27-phimaterial
title: '[M-02] Insecure Generation of Randomness Used for Token Determination Logic'
vuln_class: []
---

# [M-02] Insecure Generation of Randomness Used for Token Determination Logic

_Section severity (from Solodit section header): Medium_  
_Audit firm: Shieldify_  
_Source report: [2023-07-27-PHIMaterial.md](https://github.com/solodit/solodit_content/blob/main/reports/Shieldify/2023-07-27-PHIMaterial.md)_

---

**Severity**

Medium Risk

**Description**

`EmissionLogic.sol` contains the `determineTokenByLogic()` function that determines the rarity and `tokenId` of a `MaterialObject`.
It generates a `uint256 random` value that relies on variables like `block.timestamp` and `tx.origin` as a source of randomness is a common vulnerability, as the outcome can be predicted by calling contracts or validators. In the context of blockchains, the best and most secure source of randomness is that which is generated off-chain in a verified manner.

The function also uses `block.prevrandao` whose random seed calculation is by epoch basis, which means that entropy within 2 epochs is low and sometimes [`even predictable`](https://github.com/ethereum/annotated-spec/blob/master/phase0/beacon-chain.md#aside-randao-seeds-and-committee-generation). Users of PREVRANDAO would need to check that a validator has provided a block since the last time they called PREVRANDAO. Otherwise, they won't necessarily be drawing statistically independent random outputs on successive calls to PREVRANDAO.

In the context of Phi's business logic, improper insecure randomness generation could allow malicious actors to mint more rare/exclusive `MaterialObject` items.

**Location of Affected Code**

File: [`src/EmissionLogic.sol#L49`](https://github.com/PHI-LABS-INC/DailyMaterial/blob/355376812ba1e2eeed97d5447c2afea83a3ca8f1/src/EmissionLogic.sol#L49)

```solidity
uint256 random = uint256(keccak256(abi.encodePacked(block.prevrandao, block.timestamp, tx.origin)));
```

**Recommendation**

Consider using a decentralized oracle for the generation of random numbers, such as `Chainlink's VRF`. It is important to take into account the `requestConfirmations` variable that will be used in the `VRFv2Consumer` contract when implementing VRF. The purpose of this value is to specify the minimum number of blocks you wish to wait before receiving randomness from the Chainlink VRF service. The inclusion of this value is motivated by the occurrence of chain reorganizations, which result in the alteration of blocks and transactions. Addressing this concern is crucial for the successful implementation of this application on the Polygon network because it is prone to block reorgs and they happen almost on a daily basis.

Shieldify recommends setting the `requestConfirmations` value to at least 5, so that the larger portion of the reorgs that happen are properly taken into account and won't impact the randomness generation.

**Team Response**

Acknowledged, but currently will not be mitigated as the team does not have plans to implement Chainlink functionality yet.
