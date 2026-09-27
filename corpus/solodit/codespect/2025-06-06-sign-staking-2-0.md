---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-2-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[L-01] APR calculation does not support fractional values'
vuln_class: []
---

# [L-01] APR calculation does not support fractional values

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol#L329)

**Description:**

A user’s stake accrues interest based on the duration it remains in the contract. Interest is calculated during each staking or unstaking action (including NFT stake/unstake events). The interest calculation is based on the time elapsed since the last checkpoint, using the following formula:

```solidity
uint256 currentPeriodInterest = (userStake.amount * currentAPY * timeElapsed) / (100 * YEAR);
```

The divisor `100 * YEAR` implies that the APR is expressed as whole percentages (e.g., 11% but not 11.5%). This restricts the protocol from setting fractional APR values, which are commonly used in DeFi systems.

Following confirmation with the Sign team, it was acknowledged that this limitation stems from the current implementation. The team agreed that the base divisor should be increased to support fractional APRs.

**Impact:** Limits the protocol’s ability to define APRs with decimal precision (e.g., 11.5%), reducing flexibility in interest rate configuration.

**Recommendation:** Increase the base denominator to enable more granular APR values (e.g., use a base of 10,000 instead of 100).

**Status:** Fixed

**Update from TokenTable:** [f97c626a7f09bf8a54d2dca2c4093a79a3ffa505](https://github.com/EthSign/sign-token-staking-evm/commit/f97c626a7f09bf8a54d2dca2c4093a79a3ffa505)
