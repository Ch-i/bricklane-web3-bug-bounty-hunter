---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: '`SecuritizeBridge::executeVAAv1` never checks `vm.consistencyLevel` so non-finalized
  VAAs can be consumed, enabling reorg-based supply inflation'
vuln_class: []
---

# `SecuritizeBridge::executeVAAv1` never checks `vm.consistencyLevel` so non-finalized VAAs can be consumed, enabling reorg-based supply inflation

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** The VAA signed by the Wormhole guardian network includes a `consistencyLevel` field that records the finality guarantee the source contract requested when it called `publishMessage`. On Ethereum the `consistencyLevel` is a guardian-interpreted sentinel, not a monotonic finality scale: `200` means instant (the guardians sign as soon as the transaction is observed, before block finality), `201` means "safe" (current default, per `contracts/bridge/SecuritizeBridge.sol:194`), and every other value - including values below `200` - is treated as finalized. `SecuritizeBridge::executeVAAv1` at `contracts/bridge/SecuritizeBridge.sol:328-400` verifies the VAA via `parseAndVerifyVM` (line 330), checks the emitter address (lines 338-340), validates replay protection (lines 358-359), and decodes the payload (lines 343-352) - but it never reads `vm.consistencyLevel`. The destination contract will accept a VAA at any consistency level, including instant.

The source-side `consistencyLevel` is owner-mutable via `updateConsistencyLevel` (`contracts/bridge/SecuritizeBridge.sol:234-237`) and is initialized to `201` at deployment (`contracts/bridge/SecuritizeBridge.sol:194`). If the owner sets it to `200` (instant), or if the current `201` "safe" level is insufficient for the source chain's finality guarantees in practice, guardians produce a valid, fully-verified VAA before the source burn transaction achieves finality. If the source chain subsequently reorgs and drops the burn transaction, the destination has already consumed the VAA and issued tokens - the investor's source-chain balance is restored while the destination mint stands. This violates the bridge's core conservation property that the total supply across all chains must not increase as a result of a bridge operation.

The in-scope contract documents the instant option explicitly at `contracts/bridge/SecuritizeBridge.sol:117` with the comment `ethereum: instant 200 - safe 201 - otherwise finalized`, confirming that a low consistency level is a supported configuration. No destination-side check closes the gap regardless of what level the source selects.

**Files:**

`SecuritizeBridge::executeVAAv1`

**Impact:** An investor can mint DS tokens on the destination chain without a finalized burn on the source chain. If the source transaction is reorganized away, the investor holds tokens on both chains for the same `value`, inflating total supply. The risk is proportional to both the probability of a source-chain reorg at the depth of the burn transaction and the consistency level configured by the owner. With `consistencyLevel = 200` (instant), a single block reorg is sufficient. With `201` ("safe"), the risk depends on the source chain's safe-head depth. Because `executeVAAv1` is permissionless, a VAA produced before finality can be delivered and consumed by anyone immediately after the guardians sign it.

**Recommended Mitigation:** In `SecuritizeBridge::executeVAAv1` for finalized-only delivery on Ethereum, reject the two non-final sentinels explicitly:
```solidity
// 200 = instant, 201 = safe; every other value is finalized
if (vm.consistencyLevel == 200 || vm.consistencyLevel == 201) revert InsufficientConsistencyLevel();
```

For a safe-or-better policy, reject only instant:
```solidity
if (vm.consistencyLevel == 200) revert InsufficientConsistencyLevel();
```

Because the acceptable classes can differ per source chain, prefer a per-source-chain allowlist (or enum) of accepted Wormhole finality classes rather than a single numeric comparison.

**Securitize:** Acknowledged; our intention is never to use instant finality in production/mainnet. We only set it to 200 in testing/testnet environments because otherwise we would need to wait around 20 minutes for every test run, which would significantly slow down development and CI execution.

So in practice instant finality is only ever used exclusively for testing purposes.
