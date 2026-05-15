---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-33
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Lambda convert logic should continue to be refined
vuln_class: []
---

# Lambda convert logic should continue to be refined

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The purpose of the `LibConvertData::ConvertKind` enum type [`LAMBDA_LAMBDA`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Convert/LibConvertData.sol#L17) is to allow the Bean Denominated Value (BDV) of a deposit to be updated without forcing the owner to first withdraw that deposit, which has the undesirable side-effect of foregoing the grown Stalk of the deposit. The token `amountIn` and `amountOut` are equal when calling [`LibLambdaConvert::convert`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Convert/LibLambdaConvert.sol#L15-L28) through [`ConvertFacet::convert`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L71), which proceeds to calculate a [new BDV](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L85) for the deposit corresponding to the existing token amount. As mentioned, this allows users to update the BDV of a deposit that is potentially stale to the downside without first withdrawing the deposit; however, by the same token, it is possible for the BDV for a deposit to be stale in such a way that its BDV is higher than it should be in reality. In this case, the user has no incentive to perform a lambda convert on their deposit because it benefits from additional seignorage than it should actually be owed given current market conditions. It is [not currently possible](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L85) for the BDV of a deposit to decrease, but it is understood that a Game Theoretic solution is intended to be implemented to allow any caller to initiate a lambda convert on the deposit of a given account that may be stale in this way. It is recommended that this solution be implemented as a temporary measure while other methods for handling this issue are explored.
