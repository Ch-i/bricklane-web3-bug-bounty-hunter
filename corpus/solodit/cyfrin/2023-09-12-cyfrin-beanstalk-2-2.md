---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Silent failure can occur in `Pipeline` function calls if the target has no
  code
vuln_class: []
---

# Silent failure can occur in `Pipeline` function calls if the target has no code

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** In the case of a `Pipeline` function call to a target address with no code, the call will silently fail. Scenarios where this may occur include calls to non-contract addresses or on a contract where its self-destruction occurs beforehand. This is most relevant when considering [`Pipeline::advancedPipe`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/pipeline/Pipeline.sol#L91) given that the next call uses as input the return from the previous call which may lead to an undesired final result or revert. Pipeline can be used standalone but it is also wrapped by Beanstalk for use within the protocol by the [DepotFacet](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/DepotFacet.sol#L15-L16).

**Impact:** Silent failure of a call to an address with no code produces a silent failure within Pipeline, which can lead to undesired final outcomes. According to the [Pipeline Whitepaper](https://evmpipeline.org/pipeline.pdf):
>The combination of Pipeline, Depot and Clipboard allows EVM users to perform arbitrary validations, through arbitrarily many protocols, in a single transaction.

This implies that Pipeline should be able to be used with any protocol; therefore, the edge case must be considered where a call to a contract that has just been self-destructed should revert. Considering the low likelihood, this issue is determined to be of **LOW** severity.

**Recommended Mitigation:** If `Pipeline` is intended to support calls to EOA, and to prevent silent failure to this kind of address, an extra attribute `isContractCall` can be added to `PipeCall` and `AdvancedPipeCall` - if the call return data size is zero, and this value is true, then it should be checked whether the call was performed on a target contract, and if not then revert.
