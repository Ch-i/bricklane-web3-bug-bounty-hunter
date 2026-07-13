---
id: synthesis-merkle-proof-verification
source: synthesis
source_url: null
title: "Merkle Proof Verification Patterns: leaf domain separation, index bounds, nullifiers, and root governance"
ingested_at: 2026-06-04T21:02:36Z
vuln_class:
  - merkle-proof
  - signature-replay
  - access-control
  - input-validation
  - dos
protocol_category:
  - airdrop
  - distribution
  - bridge
  - rollup
  - nft
  - staking
tags:
  - synthesis
  - merkle-proof
  - airdrop
  - whitelist
  - second-preimage
  - replay
derives_from:
  - solodit-pashov-audit-group-2023-02-01-metalabel-1-3
  - solodit-zokyo-2023-12-11-limit-break-1-3
  - solodit-hexens-2023-10-16-eigenlayer-0-1
  - solodit-hexens-2023-02-27-polygonzkevm-3-0
  - solodit-hexens-2023-02-27-polygonzkevm-0-1
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-1
  - solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-4
  - solodit-zachobront-2023-04-12-sound-xyz-1-0
  - solodit-zokyo-2024-06-09-elektrik-2-10
  - solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-0-0
  - solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-3
  - solodit-pashov-audit-group-2023-08-01-smoothly-2-2
  - solodit-pashov-audit-group-2023-02-01-metalabel-1-0
  - solodit-pashov-audit-group-2023-02-01-metalabel-1-1
  - rekt-hyperbridge-rekt
  - solodit-cyfrin-2024-05-24-cyfrin-linea-2-1
---

# Merkle Proof Verification Patterns

## Pattern

A Merkle proof lets a contract cheaply verify that some `leaf` belongs to a set
committed to by a single on-chain `root`, without storing the whole set. The
caller supplies the leaf data and a `bytes32[]` sibling path; the verifier
re-hashes upward (`MerkleProof.verify`) and checks the result equals the stored
root. This powers airdrops, whitelists, affiliate lists, NFT allowlists, bridge
withdrawal proofs, beacon-chain withdrawal proofs, sparse Merkle tree (SMT)
storage proofs, and Merkle Mountain Range (MMR) bridge proofs. Because the proof
data is entirely attacker-controlled, the verifier is a trust boundary: every
field that is *not* cryptographically bound into the leaf and every traversal
parameter that is *not* bounds-checked becomes a degree of freedom an attacker
can exploit to forge inclusion, replay a claim, or spend the same leaf twice.

The bug classes cluster into four families. **(1) Leaf/node ambiguity** — if
leaves are hashed the same way as internal nodes (single `keccak256` of packed
data, 64-byte preimages), an attacker can present an internal node *as* a leaf
(second-preimage attack), proving membership of data that was never in the set
([metalabel-1-3], [limit-break-1-3]). **(2) Unbounded traversal / index
manipulation** — proofs that carry an index or position (indexed Merkle trees,
multi-tree / MMR / SMT proofs) must bound that index to the tree height and
constrain path bits to `{0,1}`; otherwise the prover steers the hash chain into
unintended subtrees and forges inclusion or double-spends a slot
([eigenlayer-0-1], [polygonzkevm-3-0], [polygonzkevm-0-1], [hyperbridge]).
**(3) Missing replay protection** — a valid leaf with no nullifier (claimed
bitmap) can be consumed repeatedly, and a leaf that omits epoch/round/chain/
contract binding can be replayed against a reused or different root
([statusl2-0-1], [metalabel-1-0], [smoothly-2-2], [elektrik-2-10]). **(4) Root
lifecycle / verifier governance** — who can set or rotate the root, whether
claims pause during rotation, and whether a "no-proof" path or swappable verifier
exists, all determine whether the cryptography can be sidestepped entirely
([solidlyv3-0-0], [statusl2-0-1], [linea-2-1]).

The recurring auditing lesson is that proof *validity* (does the math check out?)
is necessary but not sufficient. The leaf must commit to **everything that
matters** — recipient, amount, index, epoch, chain id, contract — and the
verifier must reject every malformed shape (oversized index, non-binary path bit,
empty proof) by reverting rather than silently returning `false`. A single
missing bounds check is enough: Hyperbridge lost ~$2.5M and minted 1 billion DOT
from exactly one omitted line in an MMR proof verifier ([hyperbridge]).

## Variants

### V1: Leaf/internal-node ambiguity & second preimage

If leaves are single-hashed and indistinguishable in size from internal-node
concatenations, an attacker can supply an internal node's 64-byte preimage as a
"leaf" and prove membership of an element never in the tree. Metalabel hashed
leaves only once; the correct mitigation is OpenZeppelin's double-hashing of
leaves (`keccak256(bytes.concat(keccak256(abi.encode(...))))`) so leaf hashes
can never collide with internal-node hashes ([metalabel-1-3]). The same root
cause appears as OZ's explicit warning against using raw `keccak256` for leaves:
"the concatenation of a sorted pair of internal nodes could be reinterpreted as a
leaf value" — Limit Break's `CPortModule` used `keccak256` for leaf hashing and
was flagged for exactly this ([limit-break-1-3]).

### V2: Unbounded index in indexed / multi-tree / MMR proofs

When a proof carries an explicit index used to decide left/right at each level,
the index must be `< 2**treeHeight`. Polygon zkEVM's `verifyMerkleProof` took a
`uint64 index` for a 32-level tree; the high bits above level 32 were unchecked,
so the same leaf could be replayed with different high bits to double-spend
([polygonzkevm-3-0]). EigenLayer's `verifyWithdrawal` composes *several* trees
(beacon-state → historical-summaries → block-root → execution → withdrawal) by
bit-packing multiple user-supplied indices into one combined index; one of them
(`historicalSummaryIndex`) was missing its bounds check, letting an attacker
overflow it into the constant prefix bits and redirect traversal into arbitrary
beacon-state fields — forging withdrawal proofs ([eigenlayer-0-1]). Hyperbridge's
MMR verifier is the in-the-wild realization of this class: a missing bounds check
let forged proofs pass ([hyperbridge]).

### V3: Sparse-Merkle-tree path / circuit constraint gaps

SMT and zk proof systems add their own traversal constraints. Polygon zkEVM's
storage SMT proved `(key, value)` inclusion by walking key bits, but the
next-key-bit polynomial `rkeyBit` lacked a binary `{0,1}` constraint and the ROM
took the bit from a free input without asserting it was boolean — letting a
prover forge a fake inclusion in the SMT ([polygonzkevm-0-1]). The audit lesson
generalizes: any value that selects a traversal direction (index bit, path bit)
must be range-/binary-constrained, in both Solidity verifiers and circuit PIL.

### V4: Missing nullifier — leaf reuse and root reuse

A valid proof grants an action; without a consumed-marker the action repeats.
Metalabel's `mintMemberships` allowed the same leaf to be used to mint, burn, and
re-mint, inflating supply and spamming events — fix is to forbid reuse of the
same leaf ([metalabel-1-0]). Even with a per-leaf nullifier, reusing a *root*
across distribution rounds lets old leaves be replayed: Smoothly's withdrawal/
exit trees should include the `epoch` in each leaf so a reused root cannot replay
a previous epoch's leaf ([smoothly-2-2]).

### V5: Root rotation re-claim (claimed-bitmap vs. new root)

When the merkleRoot is updated to fold in previously-unclaimed users, a user who
front-runs the update by claiming under the old root, then claims again under the
new root, double-claims. Status Network's `KarmaAirdrop` inherited `Pausable` for
exactly this rotation window, but `claim()` was missing the `whenNotPaused`
modifier — so the protection was inert and double-claim was live (Critical)
([statusl2-0-1]). Audit takeaway: pausing claims during root rotation only works
if every claim entrypoint actually enforces the pause.

### V6: Missing domain/context & wrong identity bound into the leaf

Leaves must bind the full context of the claim. Elektrik's airdrop `claim()`
omitted a context header (contract address, chain id, version) in the proved
data, leaving it open to cross-context replay ([elektrik-2-10]). Metalabel bound
a user-supplied `mints[i].to` rather than `msg.sender` into the leaf, so anyone
could mint another user's membership and influence its NFT id — prefer
`msg.sender` in leaf generation ([metalabel-1-1]).

### V7: Verify-returns-false vs. revert; empty-proof default branches

`MerkleProof.verify` returns a boolean; callers that branch on it can silently
take the wrong path. In Sound.xyz, `isAffiliatedWithProof` returned `false` for
an *incorrect* or *empty* proof exactly as it does for "no affiliate," so a mint
with a wrong/empty proof silently skipped the affiliate payout with no chance to
retry — the contract could not distinguish "intentionally none" from "bad proof"
([sound-xyz-1-0]). Audit takeaway: a malformed proof should revert (or be
explicitly distinguished), not fall through into a default-allow/default-skip
branch.

### V8: Root lifecycle & verifier governance bypass

The strongest leaf binding is moot if the root or verifier is attacker-
controllable. SolidlyV3's `RewardsDistributor::triggerRoot` was permissionless
and non-resetting, so anyone could call it repeatedly to bump `lastUpdatedAt`
(blocking claims via the claim-delay check) or to overwrite `root.value` and
effectively *unpause* a paused distribution ([solidlyv3-0-0]). Linea exposed
`finalizeBlocksWithoutProof` and a settable verifier (`setVerifierAddress`) that
could point at a stub returning `true`, allowing false L2 Merkle roots to be
finalized and then used by `claimMessageWithProof` to drain L1 ETH
([linea-2-1]). Even off-path griefing counts: Status Network's `claim` wired in a
`delegateBySig` whose signature could be front-run out of the mempool, reverting
the whole claim and blocking the user ([statusl2-2-4]).

### V9: Library / implementation CVEs

The verifier you import can itself be the bug. OpenZeppelin's Merkle *Multi*Proof
(`multiProofVerify`) had a vulnerability (advisory GHSA-wprv-93r4-jj2p) fixed in
4.9.2 whereby a crafted multiproof could "prove" leaves not actually in the tree;
SolidlyV3 was advised to bump its minimum OZ from 4.5.0 to ≥4.9.2
([solidlyv3-1-3]). Audit takeaway: pin and check the version of any Merkle
library, and prefer single-leaf `verify` over `multiProofVerify` unless the
version is known-good.

## Audit checklist

- Are leaves **double-hashed** (or otherwise domain-separated) so a leaf hash can never equal an internal-node hash (second-preimage resistance)? [metalabel-1-3]
- Is leaf hashing free of the raw-`keccak256`-on-sorted-pairs ambiguity OZ warns about — i.e. is the leaf preimage guaranteed not to collide with a 64-byte internal-node concatenation? [limit-break-1-3]
- For proofs carrying an **index/position**, is the index bounds-checked `< 2**treeHeight` before traversal? [polygonzkevm-3-0], [eigenlayer-0-1]
- For **multi-tree / MMR / composed** proofs, is *every* sub-index and every proof-array length validated (no unbounded field that can overflow into prefix bits)? [eigenlayer-0-1], [hyperbridge]
- Are path-selecting bits constrained to `{0,1}` (binary constraint) in both Solidity and any zk circuit / PIL? [polygonzkevm-0-1]
- Is each leaf consumable **at most once** via a nullifier / claimed-bitmap, and does that marker survive burns/re-mints? [metalabel-1-0], [statusl2-0-1]
- Does the leaf bind an **epoch / round / version** so a reused or rotated root cannot replay a prior round's leaves? [smoothly-2-2]
- When the **root is rotated**, are claims paused and is the pause actually enforced on *every* claim entrypoint (e.g. `whenNotPaused` present)? [statusl2-0-1]
- Does the leaf bind full **domain context** — contract address, chain id, contract version — to prevent cross-chain / cross-contract replay? [elektrik-2-10]
- Is the claim identity bound to **`msg.sender`** rather than an arbitrary user-supplied recipient embedded in the leaf? [metalabel-1-1]
- On an invalid/empty proof, does verification **revert** rather than silently returning `false` into a default-allow/default-skip branch? [sound-xyz-1-0]
- Is root setting/rotation **access-controlled** and non-replayable (cannot be re-triggered to grief claims or to unpause a paused state)? [solidlyv3-0-0]
- Are there any **proof-bypass paths** — `finalize…WithoutProof`, swappable/no-op verifier addresses — that let unverified roots be accepted? [linea-2-1]
- Is the Merkle **library version** pinned to a release without known proof-forgery CVEs (OZ ≥ 4.9.2 for multiproof)? [solidlyv3-1-3]
- Are auxiliary signatures wired into the claim (e.g. `delegateBySig`/permit) wrapped so a front-run/replay of the signature can't revert or block the claim? [statusl2-2-4]

## Prior incidents

- **Hyperbridge (2026-04-13) — $2.5M**: A missing bounds check in the MMR proof verifier let forged proofs pass, minting 1 billion DOT across two attacks; "one missing line of code" defeated a bridge whose entire design promised unforgeable cryptographic proofs. [cites: rekt-hyperbridge-rekt]
- **EigenLayer (audit 2023-10-16) — caught pre-deploy (High/Critical)**: `BeaconChainProofs.verifyWithdrawal` was missing a bit-size check on `historicalSummaryIndex`; because indices are bit-packed across composed trees, an unbounded index overwrote the constant prefix and let withdrawal proofs be forged. [cites: solodit-hexens-2023-10-16-eigenlayer-0-1]
- **Polygon zkEVM (audit 2023-02-27) — caught pre-deploy**: `verifyMerkleProof` used a `uint64 index` for a 32-level tree (high bits unchecked → double-spend), and the storage SMT lacked a binary constraint on the next-key bit, enabling proof of fake SMT inclusion. [cites: solodit-hexens-2023-02-27-polygonzkevm-3-0, solodit-hexens-2023-02-27-polygonzkevm-0-1]
- **Status Network KarmaAirdrop (audit 2026-01-05) — caught pre-deploy (Critical)**: `claim()` lacked `whenNotPaused`, so during merkleRoot rotation a user could claim under the old root then re-claim the re-included leaf under the new root. [cites: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-1]
- **OpenZeppelin MerkleProof MultiProof (advisory GHSA-wprv-93r4-jj2p, fixed v4.9.2)**: prior versions of `multiProofVerify` could "prove" membership of leaves not in the tree; SolidlyV3 was advised to bump its minimum OZ to ≥4.9.2. [cites: solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-3]
- **Metalabel (audit 2023-02-01) — caught pre-deploy**: single-hashed leaves (second-preimage exposure), reusable leaves (mint/burn/re-mint), and a user-supplied recipient in the leaf instead of `msg.sender`. [cites: solodit-pashov-audit-group-2023-02-01-metalabel-1-3, solodit-pashov-audit-group-2023-02-01-metalabel-1-0, solodit-pashov-audit-group-2023-02-01-metalabel-1-1]
- **Linea (audit 2024-05-24)**: `finalizeBlocksWithoutProof` and a settable verifier allowed bypassing validity-proof verification and finalizing false L2 Merkle roots usable to drain L1 ETH via `claimMessageWithProof`. [cites: solodit-cyfrin-2024-05-24-cyfrin-linea-2-1]

## References

- solodit-pashov-audit-group-2023-02-01-metalabel-1-3 — single-hashed leaves / second-preimage; use OZ double-hashing
- solodit-zokyo-2023-12-11-limit-break-1-3 — `keccak256` leaf hashing flagged; sorted-pair node reinterpretable as leaf
- solodit-hexens-2023-10-16-eigenlayer-0-1 — missing index bit-size check on `historicalSummaryIndex` → forged withdrawal proofs
- solodit-hexens-2023-02-27-polygonzkevm-3-0 — `uint64 index` in `verifyMerkleProof` for 32-level tree → double-spend
- solodit-hexens-2023-02-27-polygonzkevm-0-1 — missing binary constraint on SMT next-key bit → fake inclusion
- solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-1 — double claim across merkleRoot rotation (missing `whenNotPaused`)
- solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-2-4 — `delegateBySig` signature front-run blocks airdrop claim
- solodit-zachobront-2023-04-12-sound-xyz-1-0 — `verify` returns false (not revert); empty/incorrect proof silently skips payout
- solodit-zokyo-2024-06-09-elektrik-2-10 — missing context header (contract/chain/version) in proved claim data
- solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-0-0 — permissionless, non-resetting `triggerRoot` blocks claims / unpauses
- solodit-cyfrin-2024-01-24-cyfrin-solidlyv3-1-3 — OZ <4.9.2 Merkle MultiProof vulnerability (GHSA-wprv-93r4-jj2p)
- solodit-pashov-audit-group-2023-08-01-smoothly-2-2 — include `epoch` in leaves to prevent root-reuse replay
- solodit-pashov-audit-group-2023-02-01-metalabel-1-0 — leaf reuse (mint/burn/re-mint); add per-leaf nullifier
- solodit-pashov-audit-group-2023-02-01-metalabel-1-1 — bind `msg.sender`, not user-supplied `to`, in the leaf
- rekt-hyperbridge-rekt — $2.5M MMR proof verifier missing bounds check, 1B DOT minted
- solodit-cyfrin-2024-05-24-cyfrin-linea-2-1 — proof-verification bypass paths enable false L2 Merkle roots
