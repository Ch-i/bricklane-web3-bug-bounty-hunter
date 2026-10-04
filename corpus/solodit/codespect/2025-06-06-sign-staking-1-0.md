---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[M-01] Cooldown mechanism is incorrectly implemented'
vuln_class: []
---

# [M-01] Cooldown mechanism is incorrectly implemented

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol)

**Description:**

The staking contract enforces a cooldown period for withdrawals. To withdraw their stake, a user must first call `unstake(...)`, which initiates a cooldown grace period. Once the period elapses, the user must call `unstake(...)` again to complete the withdrawal of their deposited stake.

However, there are two issues with this mechanism:

1. After initiating the cooldown, the user can still make additional deposits. These new deposits are not subject to a new cooldown period;
2. Stake continues to accrue interest even after the cooldown has been initiated. This creates an exploitable scenario: a user can stake SIGN tokens and immediately call `unstake(...)`—without the intention to fully unstake. The stake will keep earning interest during the cooldown, and after it ends, the user can instantly withdraw, bypassing the intended staking constraints;

**Impact:** The cooldown mechanism is flawed and can be bypassed, allowing users to game the system and withdraw stake with accumulated interest, without respecting the intended waiting period.

**Recommendation:**

- Prevent users from depositing additional tokens while an unstaking process is active;
- Stop interest accrual immediately upon initiating an unstake;

**Status:** Fixed

**Update from TokenTable:** [09bd167d69a5c1689e21b6a605715369a5e667ae](https://github.com/EthSign/sign-token-staking-evm/commit/09bd167d69a5c1689e21b6a605715369a5e667ae)
