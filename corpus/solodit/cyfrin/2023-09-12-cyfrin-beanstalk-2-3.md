---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Missing allowance in `CurveFacet`
vuln_class: []
---

# Missing allowance in `CurveFacet`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

**Description:** When liquidity is added to a Curve pool via `CurveFacet::addLiquidity`, the Beanstalk Diamond first [receives tokens](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L112-L116) from the caller and then [sets approvals](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L117) to allow the pool to pull these tokens via `ERC20::transferFrom`. Currently, in `CurveFacet::removeLiquidity`, there is no logic for setting allowances on LP tokens before [calling the pool `remove_liquidity` function](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L180-L183) as typically the pool and LP token addresses are the same, which means that the relevant burn function can be called internally; however, some pools such as 3CRV and Tri-Crypto (which are already handled differently within a [conditional block](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/CurveFacet.sol#L175)) require an allowance to call `ERC20::burnFrom` given that the pool and LP token addresses differ in these cases.

**Impact:** Callers of the `CurveFacet` may be unable to remove liquidity from the 3CRV and Tri-Crypto pools via Beanstalk.

**Recommended Mitigation:** Unless an infinite approval is already set by the Beanstalk Diamond on these pools, which does not appear to be the case and in any case is not recommended, logic to approve the corresponding pools for these LP tokens should be added to `CurveFacet::removeLiquidity` before the actual call to remove liquidity.
