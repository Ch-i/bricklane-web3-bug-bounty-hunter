---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Unused errors
vuln_class: []
---

# Unused errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

The following errors in) `https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol` are unused. Consider using or removing the unused error.


- [Line: 15](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L15) `error InvalidVerifier();`

- [Line: 18](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L18) `error InvalidExpiration();`

- [Line: 27](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L27) `error UnauthorizedOwnerOrReceiver();`

- [Line: 30](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L30) `error UnauthorizedController();`

- [Line: 45](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L45) `error AccountAlreadyVerified();`

- [Line: 49](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L49) `error NotAdminOrOperator(address account);`

- [Line: 52](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L52) `error Paused(address account);`

- [Line: 59](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L59) `error CancelDepositRequestPending();`

- [Line: 65](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L65) `error DepositRequestWasCancelled();`

- [Line: 71](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L71) `error ExceedsDepositLimit();`

- [Line: 89](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L89) `error NoDepositRequest();`

- [Line: 95](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L95) `error NoPendingDepositRequest();`

- [Line: 101](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L101) `error NoCancelDepositRequest();`

- [Line: 113](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L113) `error ProposalExpired();`

- [Line: 116](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L116) `error NoPendingProposal();`

- [Line: 122](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L122) `error AlreadyInQueue();`

- [Line: 141](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L141) `error LoanAlreadyAccepted();`

- [Line: 153](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L153) `error LoanInDefault();`

- [Line: 162](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L162) `error LoanNotAcceptedByBorrower();`

- [Line: 168](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L168) `error ZeroSharePrice();`

- [Line: 177](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L177) `error LoanNotRepaid();`

- [Line: 186](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L186) `error PaymentNotDue();`

- [Line: 192](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L192) `error RequestDepositFailed();`

- [Line: 195](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L195) `error RequestRedeemFailed();`

- [Line: 210](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L210) `error BorrowerNotSet();`

- [Line: 213](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L213) `error PriceOracleNotSet();`

- [Line: 216](https://github.com/Accountable-Protocol/audit-2025-09-accountable/blob/fc43546fe67183235c0725f6214ee2b876b1aac6/src/constants/Errors.sol#L216) `error RewardsDistributorNotSet();`

**Accountable:** Errors removed in commit [`18ce919`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/18ce919d1771bdb0951e3601c667e5608957122c)

**Cyfrin:** Verified.
