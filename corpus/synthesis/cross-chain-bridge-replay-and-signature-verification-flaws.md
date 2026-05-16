---
id: synthesis-cross-chain-bridge-replay-and-signature-verification-flaws
source: synthesis
source_url: null
title: "Cross-chain bridge replay & signature verification flaws: pattern, variants, audit checklist"
ingested_at: 2026-05-16T00:00:00Z
vuln_class:
  - signature-replay
  - cross-chain-replay
  - signature-verification
  - bridge
  - eip-712
  - nonce
  - domain-separator
  - hash-collision
  - signature-malleability
  - validator-set
protocol_category:
  - bridge
  - cross-chain
  - messaging
tags:
  - synthesis
  - bridge
  - replay
  - signature
  - eip-712
  - nonce
  - domain-separator
  - guardian-set
  - mpc
  - validator-set
derives_from:
  - solodit-zokyo-2024-02-26-tide-0-2
  - solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-3
  - solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-0-0
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0
  - solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-0
  - solodit-zokyo-2024-05-24-chainport-0-2
  - solodit-zokyo-2024-05-24-chainport-1-4
  - solodit-kann-2025-01-19-rwa-0-0
  - solodit-zokyo-2024-07-01-heurist-3-1
  - solodit-hexens-2025-02-10-train-protocol-2-0
  - solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-1
  - solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0
  - solodit-zokyo-2024-06-07-zap-1-3
  - solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-6
  - solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-1
  - rekt-anyswap-rekt
  - rekt-wormhole-rekt
  - rekt-nomad-rekt
  - rekt-kiloex-rekt
  - rekt-roninnetwork-rektii
  - rekt-poly-network-rekt2
  - rekt-saga-rekt
  - rekt-bnb-bridge-rekt
  - rekt-chainswap-rekt
  - rekt-hyperbridge-rekt
  - swc-133
  - arxiv-2601.12434
---

# Cross-chain bridge replay & signature verification flaws

## Pattern

Cross-chain bridges and any contract that consumes off-chain signatures
(permits, meta-transactions, attestations from validators/guardians,
proofs of source-chain events) collapse into the same core security
problem: **a verifier accepts a message that it should not have, either
because the signed payload is not uniquely scoped to (signer, contract,
chain, action, attempt), or because the verification logic itself can
be tricked into returning "valid" for inputs that were never authentic.**

The first family — *replay* — happens when the protocol authenticates
something but the authentication is not tightly bound to a single
(chainId, verifyingContract, function/EntryPoint, nonce, deadline,
sender, payload-hash) tuple. The signer's intent leaks: a valid
signature for "subscribe with USDC on chain A" gets reused on chain B,
or on a sibling deployment, or on a hard-forked chain, or simply twice
on the same chain because no nonce was committed in the digest
(cyfrin-securitize-onofframp-bridge, cyfrin-remora-dynamic-tokens,
zokyo-chainport, zokyo-zap, kann-rwa, cyfrin-cryptoart,
cyfrin-metamask-delegationframework1, zokyo-tide, zokyo-heurist,
hexens-train-protocol, cyfrin-beanstalk).

The second family — *verification logic flaws* — happens when the
signature/proof check itself is broken: a guardian-set or MMR/IAVL
proof verifier accepts forged inputs (Wormhole's `verify_signatures`
bypass, Nomad's `0x00` trusted root after upgrade, BNB Bridge's
forgeable IAVL proof, Hyperbridge's missing bounds check in
`CalculateRoot`, Saga's IBC precompile trusting custom messages), the
forwarder/oracle doesn't authenticate the caller at all (KiloEx
MinimalForwarder), the signing nonce-state is reused across
deployments (Anyswap V3 ECDSA `k` reuse), or the multisig threshold is
simply too low and operator keys are compromised (Poly Network 3-of-4,
Ronin 5-of-9). Hash collisions through `abi.encodePacked` over
variable-length arguments (SWC-133) and `ecrecover` malleability are
the low-level building blocks that enable several of these.

Bridges sit in the worst possible position for both families: they
typically hold pooled collateral on multiple chains, mint wrapped
assets on the destination chain on the basis of attested deposit
events, and live behind upgradable governance — so a single mistake in
verification or a single replay window translates directly into a mint
of unbacked tokens. Bridge losses dominate the historical leaderboard
of crypto incidents (over $2.8B since 2021, per
arxiv-2601.12434), with the most expensive incidents (Wormhole $326M,
BNB Bridge $586M, Nomad $190M, Ronin $624M + $12M, Anyswap $7.9M,
Hyperbridge $2.5M, Saga $7M, KiloEx $7.5M, Chainswap $4.4M, Poly
$4.4M) all reducing to one of the variants below.

## Variants

### V1: Missing nonce in the signed digest (intra-chain replay)

The signature is verified but the contract never commits a per-signer
nonce inside the hashed payload — or it stores a nonce but doesn't
check that the supplied nonce matches the expected one. The same
signature can be replayed verbatim on the same chain to execute the
same authorized action arbitrarily many times. The
`SecuritizeOnRamp::executePreApprovedTransaction` audit is the
canonical example: the function increments `noncePerInvestor` after
the fact but never requires `txData.nonce == noncePerInvestor[...]`,
so any historical signature can be replayed (severity: Critical).
Cyfrin's Remora `TokenBank::buyTokenOCP` had the same shape — the
hash covered `(investor, token, amount)` but no nonce — letting a
buyer replay one signed quote to purchase tokens "in perpetuity, an
infinite number of times." ChainPort's `LiquidityManager.preRelease`
fits here too — nonce existed but wasn't part of the signed bytes,
so it could be re-used and the `amountsPerNonce` accounting silently
overwritten.

### V2: Missing `chainId` (cross-chain replay)

The signed digest omits `block.chainid` (or the EIP-712 domain
separator omits chain id), so a signature minted on chain A is also
valid on chain B for an identical deployment of the same contract.
Audited examples include Tide's Forwarder (no chain-id check in
`_verifySig`, High), CryptoArt (signatures lacking `chainId`),
Heurist's `signatureFreeMint`, Kann's RWA `borrowAsset` /
`swapToBorrow` (a borrow signed on chain A can be re-played on chain
B because the borrow-hash omits `chainId`), and Zap's airdrop (no
chainId *and* no `address(this)` — so it replays across both chains
and sibling contracts). This variant is now considered the default
threat model for any EIP-712-style flow.

### V3: Static / cached `DOMAIN_SEPARATOR` invalidated by hard fork

The domain separator is computed once (in the constructor or
initializer) and cached as `immutable`/`constant`. After a chain
hard-forks (e.g. ETH→ETHPoW), `block.chainid` changes on one side
but the cached separator still reads the original chainId — so any
signed permit is automatically valid on both networks until the
account nonce is exhausted. Cyfrin's Beanstalk `LibTokenPermit`
finding explicitly draws the parallel to the Omni Bridge
calldata-replay exploit on ETHPoW. Hexens' Train/Layerswap
`HashedTimeLockERC20`/`HashedTimeLockEther`, and Cyfrin's Securitize
NAV vault have the same root cause. The canonical fix is the
OpenZeppelin EIP712 pattern: cache the separator *and* the chainid
it was computed under, and lazily rebuild if `block.chainid !=
cachedChainId`.

### V4: Missing `verifyingContract` / EntryPoint binding (cross-contract replay)

The signed payload omits `address(this)` (or, for 4337 accounts, the
`EntryPoint` address). Signatures are valid on any sibling
deployment of the same code or any upgraded
EntryPoint/forwarder. Zokyo's Zap airdrop and Cyfrin's MetaMask
Delegation Framework finding are the clearest cases — the latter
includes a PoC that replays a 1 ETH transfer through a freshly
deployed `EntryPoint` after a EIP-7702 implementation swap. EIP-4337
states explicitly that the userOp signature must depend on both
`chainid` and the EntryPoint address; missing either reopens this
variant. The same shape recurs in forwarders that don't pin
`address(this)` into the digest.

### V5: Initialization or upgrade leaves verifier in a permissive state

Upgrades introduce new verifier state that, if left at default
(zero/empty), trivially accepts any input.

* **Nomad ($190M)**: the upgraded Replica contract had the zero
  message-hash registered as a trusted Merkle root, so
  `process()` accepted *every* message as proven. The exploit was
  copy-pasteable on Etherscan — open enough that hundreds of
  copycat addresses participated.
* **Ronin V3 ($12M)**: the V3-to-V4 upgrade called `initializeV4`
  but skipped `initializeV3`, leaving `_totalOperatorWeight = 0`,
  which made `minimumVoteWeight` evaluate to zero and disabled
  signature validation entirely.
* **ChainSwap ($4.4M)**: the auth check could be bypassed by
  rotating the signing address each transaction — a stale
  signer-registry permitting "any new address" as a valid signer.
* Cyfrin's `__NoncesUpgradeable_init` audit on Symbiotic is the
  micro-version of the same risk: forgetting an init call leaves
  nonce-state misconfigured and weakens replay protection.

### V6: Forged proof / fake "valid" return from the verifier

Cryptographic proof verifiers that accept inputs they should not.

* **Wormhole ($326M)**: `verify_signatures` was delegated to a
  Secp256k1 precompile, but a Solana sysvar discrepancy let the
  attacker construct a `SignatureSet` from a previous transaction
  with only 0.1 ETH and have it accepted, then call
  `complete_wrapped` to mint 120k whETH.
* **BNB Bridge ($586M)**: the IAVL proof verifier was forgeable —
  the attacker submitted a falsified proof of deposit for a
  two-year-old block on the legacy Beacon Chain and minted two
  batches of 1M BNB each.
* **Hyperbridge ($2.5M)**: `MerkleMountainRange.CalculateRoot()`
  had no `require(leaf_index < leafCount)` bounds check; an
  out-of-bounds `leaf_index` with `proof[0] == expected_root`
  caused the function to return `proof[0]`, so any forged message
  was accepted, the attacker became admin of the bridged DOT
  token, and minted 1B DOT. Auditors had flagged that the custom
  Solidity merkle libraries needed specialist review; the warning
  was ignored.
* **Saga ($7M)**: the IBC precompile validated "received" as
  "verified" — a helper contract emitted fabricated IBC payloads
  for Colt/Mustang, the bridge minted $D against fictional
  collateral, attacker redeemed for real assets and bridged out.
  Cosmos Labs later confirmed the root cause sits in Ethermint's
  shared codebase, so the bug class extends to multiple EVM
  chains.
* **KiloEx ($7.5M)**: the MinimalForwarder accepted forged
  signatures with *zero* validation, letting anyone push oracle
  prices and open/close leveraged positions on five chains in
  parallel.

### V7: ECDSA-level mistakes (k-reuse, malleability)

* **Anyswap V3 ($7.9M)**: an MPC implementation reused the
  random `k` value across two BSC transactions, allowing the
  private key to be back-calculated. (Known issue since the
  2010 fail0verflow PS3 attack.) Any signing flow that derives
  `k` insecurely — including custom nonce schemes that scan
  previous signatures — inherits this risk.
* **`ecrecover` malleability**: a third party can flip `(r,s,v)`
  to a second valid `(r,s',v')` for the same digest. If the
  contract uses the raw signature bytes as a replay-protection
  key (rather than committing a digest+nonce), the second
  signature gets through. The recommended mitigation is
  OpenZeppelin's `ECDSA.recover`/`tryRecover` (which enforces the
  EIP-2 low-S rule) plus a digest- or nonce-based replay guard.

### V8: Hash collision via `abi.encodePacked` over variable-length args (SWC-133)

`keccak256(abi.encodePacked(a, b))` for dynamic arrays can produce
identical hashes when elements are shuffled between `a` and `b`. In a
signature-verification context (e.g. `keccak256(abi.encodePacked(admins,
regularUsers))` as in the SWC-133 sample), an attacker can move
addresses from `regularUsers` into `admins` and present the same
signature — privilege-escalating their own address into the admin
list. Mitigation: use `abi.encode`, or fixed-length arrays, and never
mix multiple dynamic args inside `encodePacked` when the result is
signed.

### V9: Compromised / under-thresholded validator (multisig/MPC/guardian) set

When proof verification *is* sound, the attacker simply takes over the
signing set. This is the dominant root cause of the largest bridge
losses: Ronin 1 ($624M, 5-of-9 validator keys), Poly Network REKT 2
($4.4M, 3-of-4 compromised), Harmony Horizon ($100M, key compromise),
IoTeX/iotube, plus the original Ronin sequel where the upgrade left
threshold weight at zero. ChainPort's ChainportMainBridge audit echoes
the same theme on a smaller scale: fee validation delegated to a
single off-chain signer, with no on-chain bounds. arxiv-2601.12434
frames this as the systemic risk that motivates "Contained
Degradation" bridge designs — bridges have no graceful failure mode
between "fully operational" and "catastrophically compromised."

### V10: Time-bounded verifier state — expired guardian sets, stale fees

Even a sound verifier can produce silent denial-of-service if signed
artifacts live longer than the verifier's accepted state window.
Cyfrin's Wormhole CCTP audit highlights that in-flight VAAs signed
under the previous Guardian set fail after a 24-hour expiry — burning
the source-chain USDC without enabling the destination mint. ChainPort
audits also note that signed-fee replays are bounded only by
`deadline`, leaving a short replay window where stale fees can be
re-used. Inverse failure mode of V1/V2: instead of "signature lives
forever," the signature dies at an unsafe moment and traps user funds.

## Audit checklist

For every signature-verification path in scope, ask:

* Does the signed digest commit **all** of: `chainId`, `verifyingContract`
  (`address(this)`), action selector / type-hash, sender, payload, nonce,
  and deadline? (V1, V2, V4)
* For EIP-4337 / 7702 accounts: does the digest also commit the
  `EntryPoint` address? (V4)
* Is the `DOMAIN_SEPARATOR` recomputed if `block.chainid !=
  cachedChainId`, or built dynamically from `block.chainid`? (V3)
* Is the supplied nonce **compared against** the expected per-signer
  nonce *before* execution, not merely incremented after? (V1)
* Is the signature hash built with `abi.encode` (not
  `abi.encodePacked`) whenever multiple variable-length arguments are
  involved? (V8)
* Is `ECDSA.recover` (with low-S enforcement) used instead of raw
  `ecrecover`, and is replay protection digest-based rather than
  signature-byte-based? (V7)
* Is `recover(...) != address(0)` guarded? (general)
* On contract upgrade, are **all** new init functions (V4, V5, etc.)
  invoked, and do any new verifier knobs (trusted roots, validator
  weights, nonce mappings) have sensible non-zero defaults? Is there a
  test that a zero/empty value cannot be replayed as
  "valid/proven/zero-threshold"? (V5)
* For cross-chain message verifiers (MMR, IAVL, merkle, BEEFY): do
  bounds, length, and inclusion checks exist for every untrusted input
  field (`leaf_index`, `leafCount`, peak indices, sub-tree offsets)?
  Has the verifier library been fuzzed or specialist-reviewed
  independently of the application that calls it? (V6)
* Does the verifier reject early-exit paths whose preconditions can be
  forced by attacker-controlled inputs (e.g. Hyperbridge's
  single-leaf early return triggered by `leaf_index=1, leafCount=1`)?
  (V6)
* Are validator/guardian/MPC sets above the assumed Byzantine
  threshold, and is key-rotation/expiry semantics tested against the
  in-flight message lifetime? (V9, V10)
* For pre-release / liquidity / off-chain-attested fee flows: is the
  nonce *part of the signature payload* (not merely tracked
  off-chain)? (V1, V9)
* Does the MPC / threshold-signing implementation generate `k`
  randomly per signature, and is it resistant to fault/restore
  injection (delete-file, restore-backup, server-migration)? (V7)
* For 4337 / forwarder / meta-tx entry points: does *any* function
  on the entry point require signature verification with full
  domain binding before forwarding calls? (KiloEx-style absent
  check is the worst case.) (V6)
* On hard-fork response: is there a documented operational plan
  (pause, rotate guardian set, replay-protect) and does it work
  without unilaterally trusting an off-chain operator? (V3, V10)

## Prior incidents

- **Wormhole (Feb 2022) — $326M**: Solana `verify_signatures` accepted
  a `SignatureSet` constructed from a previous transaction due to a
  precompile/library mismatch; attacker minted 120k whETH unbacked
  [cites: rekt-wormhole-rekt].
- **Ronin Bridge I (Mar 2022) — $624M** *(referenced in
  rekt-roninnetwork-rektii / rekt-poly-network-rekt2)*: 5-of-9
  validator keys compromised, no signing diversity assumption held —
  the canonical V9 case.
- **Harmony Horizon (Jun 2022) — $100M**: validator-key compromise of
  a low-threshold multisig bridge [cites: rekt-roninnetwork-rektii,
  rekt-poly-network-rekt2].
- **Nomad (Aug 2022) — $190M**: post-upgrade Replica contract treated
  the zero hash as a trusted Merkle root; every `process()` call
  succeeded by default. Exploit was copy-pasteable, leading to
  crowd-hack [cites: rekt-nomad-rekt].
- **BNB Bridge (Oct 2022) — $586M**: forgeable IAVL proof of a
  two-year-old Beacon Chain block let the attacker mint 2× 1M BNB
  [cites: rekt-bnb-bridge-rekt].
- **Poly Network II (Jul 2023) — $4.4M**: 3-of-4 multisig key
  compromise; forged proofs across 10 chains, ~$42B notional minted
  but limited by destination liquidity [cites: rekt-poly-network-rekt2].
- **Ronin Bridge II (Aug 2024) — $12M**: V3→V4 upgrade skipped
  `initializeV3`, leaving operator weight at zero and disabling
  `minimumVoteWeight` enforcement [cites: rekt-roninnetwork-rektii].
- **KiloEx (Apr 2025) — $7.5M**: MinimalForwarder accepted forged
  signatures with no data validation; oracle price set arbitrarily on
  Base, BNB, opBNB, Taiko, Manta in parallel
  [cites: rekt-kiloex-rekt].
- **Hyperbridge (Apr 2026) — $2.5M**: missing
  `require(leaf_index < leafCount)` in custom MMR library; forged
  proofs accepted, attacker became admin of bridged DOT token on
  Ethereum and minted 1B DOT. Auditors had explicitly recommended
  specialist review of the Solidity libraries
  [cites: rekt-hyperbridge-rekt].
- **Saga (Jan 2026) — $7M**: IBC precompile trusted custom messages
  without source-chain verification; $7M Saga Dollar minted from thin
  air, depeg to $0.73. Cosmos Labs confirmed bug class is shared
  across Ethermint-based EVM chains [cites: rekt-saga-rekt].
- **Anyswap V3 (Jul 2021) — $7.9M**: ECDSA `k` reuse across two BSC
  signatures let the attacker recover the MPC private key
  [cites: rekt-anyswap-rekt].
- **ChainSwap (Jul 2021) — $4.4M**: signer-authentication used a stale
  registry that allowed any newly seen address as a valid signature,
  enabling 20 token minting flows on BSC [cites: rekt-chainswap-rekt].
- **Omni Bridge calldata replay on ETHPoW** *(referenced in
  cyfrin-beanstalk-1-0)*: cached `DOMAIN_SEPARATOR` valid on both
  forked chains; the prototype hard-fork replay case.

## References

The full corpus entries underlying this synthesis (also listed in
`derives_from`):

* solodit-zokyo-2024-02-26-tide-0-2 — chain-id missing from forwarder
  domain separator (High)
* solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-3
  — static `DOMAIN_SEPARATOR` (Low)
* solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-0-0
  — missing nonce *comparison* despite presence in digest (Critical)
* solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0 — `LibTokenPermit`
  hard-fork replay (Medium)
* solodit-cyfrin-2025-04-24-cyfrin-cryptoart-v2-0-2-0 — cross-chain
  replay, `chainId` missing
* solodit-zokyo-2024-05-24-chainport-0-2 — `LiquidityManager`
  nonce-not-in-signature (High)
* solodit-zokyo-2024-05-24-chainport-1-4 — fee-signature replay window
  bounded only by deadline
* solodit-kann-2025-01-19-rwa-0-0 — cross-chain replay in
  `borrowAsset` / `swapToBorrow` (High)
* solodit-zokyo-2024-07-01-heurist-3-1 — `signatureFreeMint` cross-domain
  replay
* solodit-hexens-2025-02-10-train-protocol-2-0 — immutable
  `DOMAIN_SEPARATOR` after hard fork (Layerswap V8 HTLC)
* solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-1 —
  `TokenBank`/`AllowList` signatures reusable in perpetuity (Critical)
* solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-0-0
  — EntryPoint not included in user-op hash (High, with PoC)
* solodit-zokyo-2024-06-07-zap-1-3 — airdrop signature lacks both
  chainId and `address(this)`
* solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-6 — expired
  Wormhole Guardian set causes in-flight VAA DoS
* solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-1 —
  `__NoncesUpgradeable_init` not invoked
* rekt-anyswap-rekt — $7.9M, ECDSA k-reuse
* rekt-wormhole-rekt — $326M, `verify_signatures` precompile bypass
* rekt-nomad-rekt — $190M, zero-root trusted after upgrade
* rekt-kiloex-rekt — $7.5M, MinimalForwarder no-sig-check
* rekt-roninnetwork-rektii — $12M, missed `initializeV3` after upgrade
* rekt-poly-network-rekt2 — $4.4M, 3-of-4 multisig compromise
* rekt-saga-rekt — $7M, IBC precompile forged messages (Ethermint
  ecosystem bug)
* rekt-bnb-bridge-rekt — $586M, forgeable IAVL proof
* rekt-chainswap-rekt — $4.4M, signer-registry replay
* rekt-hyperbridge-rekt — $2.5M, MMR `CalculateRoot` missing bounds
  check
* swc-133 — Hash collisions with multiple variable-length args
  (`abi.encodePacked`)
* arxiv-2601.12434 — ASAS-BridgeAMM; framing of cross-chain bridges as
  the single largest source of systemic DeFi risk ($2.8B since 2021)
  and the case for graceful-degradation bridge designs
