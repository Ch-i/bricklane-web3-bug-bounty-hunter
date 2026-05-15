---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Spender can front-run calls to modify token allowances, resulting in DoS and/or
  spending more than was intended
vuln_class: []
---

# Spender can front-run calls to modify token allowances, resulting in DoS and/or spending more than was intended

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** When updating the allowance for a spender that is less than the value currently set, a well-known race condition allows the spender to spend more than the caller intended by front-running the transaction that performs this update. Due to the nature of the `ERC20::approve` implementation and [other](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ApprovalFacet.sol#L46-L54) [variants](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/TokenFacet.sol#L104-L110) [used](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/MarketplaceFacet.sol#L244-L252) within the Beanstalk system, which update the mapping in storage corresponding to the given allowance, the spender can spend both the existing allowance plus any 'additional' allowance set by the in-flight transaction.

For example, consider the scenario:
* Alice approves Bob 100 tokens.
* Alice later decides to decrease this to 50.
* Bob sees this transaction in the mempool and front-runs, spending his 100 token allowance.
* Alice's transaction executes, and Bob's allowance is updated to 50.
* Bob can now spend an additional 50 tokens, resulting in a total of 150 rather than the maximum of 50 as intended by Alice.

Specific functions named `decreaseTokenAllowance`, intended to decrease approvals for a token spender, have been introduced to both the [`TokenFacet`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/TokenFacet.sol#L133-L154) and the [`ApprovalFacet`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ApprovalFacet.sol#L84-L93). [`PodTransfer::decrementAllowancePods`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/market/MarketplaceFacet/PodTransfer.sol#L87-L98) similarly exists for the Pod Marketplace.

The issue, however, with these functions is that they are still susceptible to front-running in the sense that a malicious spender could force their execution to revert, violating the intention of the caller to decrease their allowance as they continue to spend that which is currently set. Rather than simply setting the allowance to zero if the caller passes an amount to subtract that is larger than the current allowance, these functions halt execution and revert. This is due to the following line of shared logic:

```solidity
require(
    currentAllowance >= subtractedValue,
    "Silo: decreased allowance below zero"
);
```

Consider the following scenario:
* Alice approves Bob 100 tokens.
* Alice later decides to decrease this to 50.
* Bob sees this transaction in the mempool and front-runs, spending 60 of his 100 token allowance.
* Alice's transaction executes, but reverts given Bob's allowance is now 40.
* Bob can now spend the remaining 40 tokens, resulting in a total of 100 rather than the decreased amount of 50 as intended by Alice.

Of course, in this scenario, Bob could have just as easily front-run Alice's transaction and spent his entire existing allowance; however, the fact that he is able to perform a denial-of-service attack results in a degraded user experience. Similar to setting maximum approvals, these functions should handle maximum approval revocations to mitigate against this issue.

**Impact:** Requiring that the intended subtracted allowance does not exceed the current allowance results in a degraded user experience and, more significantly, their loss of funds due to a different route to the same approval front-running attack vector.

**Recommended Mitigation:** Set the allowance to zero if the intended subtracted value exceeds the current allowance.

\clearpage
