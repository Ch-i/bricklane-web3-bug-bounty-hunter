---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-12
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Missing zero-address and zero-amount input validation across constructors,
  initializers and setters
vuln_class: []
---

# Missing zero-address and zero-amount input validation across constructors, initializers and setters

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Grouping of missing non-zero / input-validation checks across constructors, initializers, and two-step setters. Each sub-item is a distinct instance.

---

**1. `TokensHolder` constructor lacks non-zero validation on `stakingVault` and `hilbtc`**

Constructor stores whatever is passed. With `stakingVault == 0`, the `onlyStakingVault` gate rejects all callers - cooldown funds permanently stuck. With `hilbtc == 0`, `HILBTC.transfer(...)` reverts on codeless call. Contract is non-upgradeable so a bad init is unrecoverable.

Source: `issuance/src/helpers/TokensHolder.sol:19-22`.

**Recommended:** `require(stakingVault != address(0) && hilbtc != address(0), AddressCantBeZero())`.

---

**2. `Minter::requestOwnerMint`, `Minter::initialize`, `StakingVault::initialize` missing non-zero checks**

`Minter::initialize` zero-checks every address except `_distributor` - a zero-init `distributor` combined with the `setDistributor` zero-skip branch allows the very first distributor assignment to skip the waiting period entirely. `requestOwnerMint` accepts any `amount` (including 0) and any `to` (including `address(0)` - causes a stale request to revert on execute, DoSing owner-mint until re-requested). `StakingVault::initialize` has the same `_distributor != 0` omission: if passed zero, `getUnvestedAmount()` reverts on the external `IDistributor(0).vestingPeriod()` call, bricking `totalAssets()` and every ERC-4626 path until admin calls `setDistributor`.

Sources: `issuance/src/minter/Minter.sol:137-188, 219-228`.

**Recommended:** Add `require(_distributor != address(0), AddressCantBeZero())` in BOTH `Minter::initialize` AND `StakingVault::initialize`. Add `require(to != address(0) && amount > 0, InvalidRequest())` in `requestOwnerMint`.

---

**3. Two-step setters missing `pendingChange.timestamp != 0` guard**

Setters read `pendingChange.newAddr` and execute without guarding against `pendingChange.timestamp == 0`. A double-executed `set*` call reads `newAddr = 0` and `timestamp = 0`; `0 + waitingPeriod <= block.timestamp` is trivially true; roles are granted to `address(0)`, bricking future functionality until another request cycle.

Sources: `issuance/src/minter/Minter.sol:301-347, 362-375`; `issuance/src/token/HilToken.sol:126-141`.

Affects `Minter::setCustodian`, `Minter::setPauser`, `Minter::setDistributor`, `HilToken::setMinter`.

**Recommended:** Add `require($.pendingChange.timestamp != 0, NoPendingRequest())` to every executor.

---

**Syntetika:** Fixed in commit [`256aa81`](https://github.com/SyntetikaLabs/monorepo/commit/256aa8101d9bcb6ebf0e43f26a58282c93506e7b), no check for distributor is intentional

**Cyfrin:** Verified.
