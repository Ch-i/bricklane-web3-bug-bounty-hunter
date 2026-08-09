---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-17-cyfrin-stbl-ess-v2-0-4-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-06-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-17-cyfrin-stbl-ess-v2-0
title: '`STBL_YLD_SplitMerge::split` and `merge` lack `nonReentrant` guard — reentrancy
  surface is real but currently blocked only by a coincidental `_safeMint` execution
  ordering in `STBL_YLD`'
vuln_class: []
---

# `STBL_YLD_SplitMerge::split` and `merge` lack `nonReentrant` guard — reentrancy surface is real but currently blocked only by a coincidental `_safeMint` execution ordering in `STBL_YLD`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-17-cyfrin-stbl-ess-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-17-cyfrin-stbl-ess-v2.0.md)_

---

**Description:** `STBL_YLD_SplitMerge::split` and `merge` carry no reentrancy guard. Both functions call `iSTBL_YLD::mint`, which internally invokes `_safeMint` — the OpenZeppelin primitive that transfers the token and then calls `IERC721Receiver::onERC721Received` on any contract recipient before returning. Any contract that receives a freshly split or merged YLD NFT therefore gains execution control mid-function, with the original call still in progress on the call stack.

The attack surface this creates is real: an attacker contract implementing `IERC721Receiver` can receive a split output, reenter `split` or `merge` on the same or a different token, and attempt to corrupt yield-staking state. The specific exploitation goal is to force `enableYield` to be called on a burned token ID, registering a ghost staker in `STBL_T1_YieldDistributor` whose yield balance accumulates permanently but can never be claimed — inflating `totalSupply` in the distributor and diluting yield for every legitimate NFT holder.

**The attack is not currently exploitable, but only by sheer luck in the ordering of two lines inside `STBL_YLD::mint`:**

```solidity
// STBL_YLD.sol lines 195–199
nftCtr += 1;
_safeMint(_to, nftCtr);          // line 197 — onERC721Received fires HERE
nftMetaData[nftCtr] = _metadata; // line 199 — metadata written AFTER callback
```

Because `_safeMint` fires the callback on line 197 and the metadata is written on line 199, the freshly minted token's `nftMetaData` is entirely zero-initialized during any reentrant call. This zero state incidentally blocks every harmful reentry path:

- **Inner `split(tokenB)`** requires `_splitAssetValue < meta.stableValueNet`. With `stableValueNet = 0`, any nonzero split value satisfies `>= 0` — a `uint256` tautology that unconditionally reverts.
- **Inner `merge(tokenB, tokenZ)`** requires `metaB.assetID == metaA.assetID`. With `metaB.assetID = 0` and the registry assigning IDs starting from 1 (ID 0 is explicitly rejected), no real token can satisfy this equality — the revert is guaranteed.

**This protection is not the result of deliberate defensive programming. It is a side-effect of statement ordering that carries no documentation, no test coverage, and no guarantee of preservation across upgrades.** `ReentrancyGuard` is already imported in `STBL_YLD_SplitMerge` but is not applied to either `split` or `merge`.

**Proof of Concept:** The exact reentrant attack that would succeed if the incidental protection were removed:

1. Attacker contract owns `tokenA` with yield enabled (`stakingData[tokenA].balance > 0`).
2. Attacker calls `split(tokenA, v)`.
3. `tokenA` is burned. `tokenB = YLD.mint(caller, metaB)` fires `_safeMint`.
4. Inside `onERC721Received`: attacker calls `split(tokenB, v2)`.
   - `tokenB` is burned; `tokenC` and `tokenD` are minted.
   - `issuer.disableYield(tokenB)` executes — reads tokenB's metadata (still in storage after burn, `isDisabled = true` but `stableValueNet` intact), calls `disableStaking(tokenB, vB)`.
   - `issuer.enableYield(tokenC)` and `issuer.enableYield(tokenD)` execute.
5. Execution returns to the outer split. `tokenE = YLD.mint(caller, metaE)` is minted.
6. `issuer.disableYield(tokenA)` executes.
7. `issuer.enableYield(tokenB)` — **tokenB is burned**. Its metadata is still readable (`isDisabled = true`, `stableValueNet = vB`). `enableStaking(tokenB, vB)` registers a ghost staker with weight `vB`.
8. `issuer.enableYield(tokenE)` executes.

Result: `stakingData[tokenB].balance = vB` with `tokenB` burned. `claim(tokenB)` always reverts because `MetaData.isDisabled == true`. The distributor's `totalSupply` is permanently inflated by `vB`, diluting all legitimate stakers proportionally for the lifetime of the pool. The attack is repeatable.

This scenario is currently unreachable only because step 4's inner `split(tokenB, v2)` reverts at input validation (zero `stableValueNet`). If `STBL_YLD.mint` is ever modified — for example, to write metadata before calling `_safeMint` — the protection silently disappears and the attack above becomes fully executable by any YLD holder deploying a contract receiver.

**Recommended Mitigation:** Apply `nonReentrant` from the already-imported `ReentrancyGuard` to both `split` and `merge`. This eliminates the latent risk regardless of future changes to `STBL_YLD::mint` and makes the protection explicit rather than dependent on statement ordering in an external contract.

**STBL:** Acknowledged.
