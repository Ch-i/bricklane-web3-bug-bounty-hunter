---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-1-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: NatSpec enhancements
vuln_class: []
---

# NatSpec enhancements

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** * [`SDLVesting#L11`](https://github.com/stakedotlink/contracts/blob/3462c0d04ff92a23843adf0be8ea969b91b9bf0c/contracts/vesting/SDLVesting.sol#L11): `beneficary` should be `beneficiary`
* [`SDLVesting::onlyBeneficiary#L90`](https://github.com/stakedotlink/contracts/blob/3462c0d04ff92a23843adf0be8ea969b91b9bf0c/contracts/vesting/SDLVesting.sol#L90): extra space in `not  beneficiary`
* [`SDLVesting::setLockTime#L187`](https://github.com/stakedotlink/contracts/blob/3462c0d04ff92a23843adf0be8ea969b91b9bf0c/contracts/vesting/SDLVesting.sol#L187): `_lockTime lock time in seconds` should be `_lockTime lock time in years`
* [`SDLVesting::vestedAmount`](https://github.com/stakedotlink/contracts/blob/3462c0d04ff92a23843adf0be8ea969b91b9bf0c/contracts/vesting/SDLVesting.sol#L195-L198): Doesn't document the return: `@return amount of tokens vested at the given timestamp. Returns full allocation if terminated.`

**Stake.Link:** Fixed in commits [`e458512`](https://github.com/stakedotlink/contracts/commit/e4585124c05137848196d4ca759c3e9d28b963e1) and [`565b043`](https://github.com/stakedotlink/contracts/commit/565b043b98f6b0a61a9eda9b7f2ca20ecdac8598)

**Cyfrin:** Verified.

\clearpage
