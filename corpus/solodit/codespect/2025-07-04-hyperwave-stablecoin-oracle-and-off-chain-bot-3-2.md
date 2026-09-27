---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-03] Improve front-running mitigations for solve(...)'
vuln_class: []
---

# [I-03] Improve front-running mitigations for solve(...)

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`AtomicQueue.sol`](https://github.com/SwellNetwork/boring-vault/blob/cff94e7093a688578d13279748cdaa0d2b308293/src/atomic-queue/AtomicQueue.sol)

**Description:**

The current design of `AtomicQueue` is prone to front-running attacks, as acknowledged in the `@dev` comment of the `solve(...)` function: _“It is very likely solve TXs will be front run if broadcasted to public mem pools, so solvers should use private mem pools.”_

When `solve` is called, an attacker may update their withdrawal request in the same block to either:

- Gain a more favourable price ratio, or;
- Cause the entire batch to revert by exceeding the `maxAssets` limit supplied by the solver bot;

This introduces a potential attack surface that could disrupt the batch execution or unfairly benefit malicious actors.

To mitigate this, the `AtomicQueue` design should be adjusted to include a delay mechanism. For example, a request must exist in the system for a minimum duration (e.g., X seconds) before it becomes solvable.

**Impact:** Front-running of atomic request updates could lead to unfair price execution for a user or complete transaction failure due to batch reverts.

**Recommendation:** Consider enforce a rule that requests can only be solved after a certain time period has passed since their submission.

**Status:** Fixed

**Client response:** Fixed in [1503d53e5517df71602468a30984860ddd3064e4](https://github.com/SwellNetwork/boring-vault/commit/1503d53e5517df71602468a30984860ddd3064e4) (contract side) and [5eedc610bb1d0e9df64e366067ccbc297cc3f9c0](https://github.com/SwellNetwork/hlp-internal-be/commit/5eedc610bb1d0e9df64e366067ccbc297cc3f9c0#diff-db2ad265c7a4170665800a49c0939fc27aebc72ef3fdf771ac0f8e8321f5fb1aR301) (off-chain bot side).
