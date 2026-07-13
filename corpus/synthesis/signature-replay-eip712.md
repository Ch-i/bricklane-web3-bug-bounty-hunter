---
id: synthesis-signature-replay-eip712
source: synthesis
source_url: null
title: "Signature Replay & EIP-712 Typed Data: pattern, variants, audit checklist"
ingested_at: 2026-06-04T00:00:00Z
vuln_class:
  - signature-replay
  - authentication
  - access-control
  - cross-chain-replay
protocol_category:
  - erc20-permit
  - bridge
  - rwa
  - airdrop
tags:
  - synthesis
  - signature-replay
  - eip712
  - permit
  - domain-separator
  - nonce
derives_from:
  - solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0
  - solodit-zokyo-2024-03-25-planar-finance-0-2
  - solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-0-0
  - solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-1
  - solodit-zokyo-2024-02-26-tide-0-2
  - solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-0-2
  - solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-3
  - solodit-hexens-2025-02-10-train-protocol-2-0
  - solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-1
  - solodit-zokyo-2024-07-01-heurist-3-1
  - solodit-zokyo-2024-06-07-zap-0-0
  - solodit-zokyo-2024-06-30-devve-0-3
  - solodit-zachobront-2023-04-15-hook-1-3
  - solodit-hexens-2024-09-19-stakewise-1-0
  - solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-1-0
  - rekt-anyswap-rekt
  - rekt-trustedvolumes-rekt
  - swc-133
---

# Signature Replay & EIP-712 Typed Data

## Pattern

Many protocols let an off-chain signer authorize an on-chain action: an
ERC-2612 `permit`, a meta-transaction forwarder, a gasless airdrop claim,
an RFQ order, an exchange/issuer pre-approval, or a staking authorization.
The contract recovers a signer from a digest (`ecrecover` / `ECDSA.recover`
/ `_hashTypedDataV4`) and acts if the signer is authorized. The entire
security of this flow rests on the digest binding the signature to a
**single, specific, one-time use**. When any binding dimension is missing,
the same signature authorizes more than the signer intended — that is
signature replay.

EIP-712 exists to make the bound digest unambiguous. The digest is
`keccak256("\x19\x01" || domainSeparator || hashStruct(message))`, where the
domain separator commits to `name`, `version`, `chainId`, and
`verifyingContract` (optionally a `salt`), and `hashStruct` commits to the
typed message fields. Replay bugs appear whenever one of these commitments
is absent, wrong, mutable, or computed once and frozen. The four binding
dimensions that matter are: **uniqueness** (a nonce so a given message can
only execute once), **chain** (`chainId` so a signature on one chain or a
post-fork chain isn't valid on another), **contract/domain** (the correct
`verifyingContract` and a salt/instance id so signatures don't cross
between deployments), and **content integrity** (the struct hash must
unambiguously commit to every security-relevant field).

A subtle but recurring trap is the *partial* nonce: a nonce is included in
the signed message and the contract even increments a stored counter, yet
it never asserts that the supplied nonce equals the expected nonce. The
signature stays replayable because nothing rejects the stale value. The
mirror image is the *frozen* domain separator: it is computed correctly at
deployment but cached as a constant/immutable, so a chain hard fork (which
changes `block.chainid`) — or a mutable token `name` — silently breaks the
binding and reopens replay.

Below the EIP-712 layer there are also raw-ECDSA failures: reusing the
signing nonce `k` across two signatures leaks the private key (Anyswap),
and `abi.encodePacked` with multiple variable-length arguments can collide
so a different parameter set produces the same digest (SWC-133). Both let
an attacker forge or reuse authorization without ever breaking the typed-
data envelope.

## Variants

### V1: No nonce / no replay protection in the signed payload

The struct hash omits any uniqueness field, so a single valid signature
authorizes the action an unbounded number of times. In Remora's `TokenBank`
the `BUY_TOKEN_TYPEHASH` hash committed only to `investor`, `token`, and
`amount` — "no nonce on the hash of the signature" — so an off-chain-paid
purchase signature could be reused in perpetuity (Critical). The Zap
airdrop let a user replay the same claim signature every week with no upper
bound, draining rewards meant for others (High). Planar Finance's
`UniswapV2ERC20.permit` had no nonce check at all (Medium).

### V2: Nonce present in the message but never enforced

Worse than obviously missing protection because it looks safe. Securitize's
`SecuritizeOnRamp::executePreApprovedTransaction` verified the EIP-712
signature over a payload that *contained* a nonce, then did
`noncePerInvestor[...] = noncePerInvestor[...] + 1` — but never checked
`txData.nonce == noncePerInvestor[txData.senderInvestor]` before executing.
Old valid signatures replay with their original nonce values, executing
duplicate subscriptions (Critical). The defense is to assert the supplied
nonce equals the expected stored nonce *before* acting, then consume it.

### V3: Cross-chain and post-fork replay (chainId binding failures)

A signature valid on one chain is accepted on another, or on a forked chain
after `block.chainid` changes. Two sub-cases:

- **Frozen/constant chainId in the domain separator.** Beanstalk's
  `LibTokenPermit::_buildDomainSeparator` used a static `CHAIN_ID`
  constant, so after a hard fork "all signed permits from Ethereum mainnet
  can be replayed on the forked chain" (Medium; the report explicitly
  draws the parallel to the Omni Bridge calldata replay on ETHPoW). Train
  Protocol's `DOMAIN_SEPARATOR` was a constructor-set immutable and "becomes
  invalid after a hard fork" (Low). Securitize's redeem-swap vault set
  `DOMAIN_SEPARATOR` once at init with `block.chainid` baked in (Low). The
  canonical fix is OpenZeppelin's `EIP712`, which recomputes the separator
  when `block.chainid` differs from the cached id.
- **chainId / domain not validated at all.** Tide's `Forwarder._verifySig`
  never compared the domain separator's chain id against the contract's
  current chain id, allowing cross-chain replay (High). Heurist's
  `signatureFreeMint` omitted contract address and chain id from the signed
  data entirely, allowing cross-domain mint replay (Informational).

### V4: Wrong or mutable domain binding (verifyingContract / name / instance)

The domain separator is dynamic but bound to the wrong value. Hook set the
EIP-712 `verifyingContract` to the `_protocol` address passed into the
constructor instead of the contract actually performing verification
(`address(this)`), corrupting every digest (Medium). Securitize's
`StandardToken` initialized the domain separator with the token `name`, but
`updateNameAndSymbol` could later change the name without recomputing the
separator — after which "100% of newly generated permit signatures will
fail validation" (a mutable-domain integrity bug; Medium). The Securitize
SVM on/off-ramp operator swap signature lacked a nonce *and* did not bind
to `on_ramp_state` / `asset_mint`, so a signature could be replayed within
its deadline and reused across on-ramp instances (Low) — i.e. missing
instance/salt binding lets one signature roam across deployments.

### V5: Hash-construction ambiguity (encoding collisions)

Even with a nonce and correct domain, the digest can be forgeable if it is
built ambiguously. SWC-133: `abi.encodePacked()` with multiple
variable-length arguments concatenates without delimiters, so elements can
be shifted between arrays to yield an identical hash and bypass signature
authorization. Remediation: use `abi.encode()`, fixed-length arrays, or
keep variable-length user-controlled fields out of the packed digest.

### V6: Raw-ECDSA and signer-authorization failures

These don't break the typed-data envelope; they attack the signature
primitive or the authorization set. Anyswap's V3 Router signed two
transactions with a repeated ECDSA nonce `k`, letting the attacker
back-calculate the MPC private key (a known class since 2010). TrustedVolumes
exposed a *public* function that let anyone register themselves as an
`AllowedOrderSigner`, and the fill path never checked whether the registered
signer actually owned the assets — turning "valid signature" into "anyone."
Both show that signature checks are only as strong as the key custody and
the signer-authorization set behind them.

### V7: Permit front-running / griefing DoS

Single-use, nonce-bound signatures can be weaponized for denial of service.
Because a `permit` is public and idempotent on the nonce, an attacker who
sees the signature in the mempool can submit it first; the victim's bundled
transaction (e.g. `permit` + action) then reverts on the already-consumed
nonce. StakeWise's `LeverageStrategy.permit()` was front-runnable, wasting
gas and DoSing the flow (Low); Securitize's `transferWithPermit` could be
DoSed by front-running a direct call to the underlying `permit` (Low). Fix:
wrap `permit` in try/catch or check existing allowance before calling.

## Audit checklist

- Does every signed message include a nonce, and is that nonce **checked
  against expected stored state and consumed before any external effect**
  (not merely incremented after recovery)?
- Is the supplied nonce asserted equal to the expected nonce *before* the
  action runs (guard against the "signs a nonce but never validates it"
  pattern)?
- Does the struct hash commit to **all** security-relevant fields (nonce,
  deadline, recipient, amount, target asset, instance id)?
- Is the EIP-712 domain separator computed from `block.chainid` and
  **recomputed when the chain id changes** (OpenZeppelin `EIP712`), rather
  than stored as a constant/immutable baked in at deploy?
- Does verification bind to the current `chainId` and verifying domain — is
  the domain separator's chain id compared against the live chain id?
- Is `verifyingContract` the contract actually performing verification
  (`address(this)`), not a proxy/protocol/forwarded address?
- If the token `name`/`version` (or any domain field) is mutable, is the
  domain separator recomputed on change — or are those fields immutable?
- Does the signed payload include a unique contract/instance identifier (or
  `salt`) so a signature cannot be replayed across separate deployments?
- When building the digest with `abi.encodePacked`, are there multiple
  variable-length arguments that could collide? Prefer `abi.encode` or
  fixed-length encoding (SWC-133).
- Is the signature bound to a `deadline`, and are deadline + nonce together
  sufficient to bound the replay window?
- Is the `permit`/meta-tx flow protected against front-running DoS
  (try/catch around `permit`, or check existing allowance first)?
- Is the signer-authorization set access-controlled (no public/permissionless
  signer registration), and does the action re-verify ownership/authority of
  the recovered signer?
- For off-chain/MPC signing, is a fresh random (or RFC-6979 deterministic)
  `k` used per signature so `k` is never reused across signatures?

## Prior incidents

- **Anyswap (2021-07-10) — $7.9M**: the V3 Router signed two BSC
  transactions with a repeated ECDSA nonce `k`, allowing the attacker to
  back-calculate the MPC private key and drain bridge liquidity. [cites: rekt-anyswap-rekt]
- **TrustedVolumes (2026-05-07) — $5.87M**: a public function let the
  attacker register as an `AllowedOrderSigner`; the RFQ fill path never
  verified the signer owned the assets, draining four assets in one tx.
  [cites: rekt-trustedvolumes-rekt]
- **Omni Bridge / ETHPoW fork replay (referenced)**: calldata/signature
  replay on a forked chain after the chain id diverged — cited by the
  Beanstalk review as the precedent for static-`CHAIN_ID` domain separators.
  [cites: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0]
- **Securitize OnRamp (2025-07, audit-caught, Critical)**: missing
  `nonce == expected` validation in `executePreApprovedTransaction` would
  have allowed replay of pre-approved subscription transactions.
  [cites: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-0-0]
- **Remora TokenBank (2025-10, audit-caught, Critical)**: off-chain-paid
  purchase signatures with no nonce in the struct hash were reusable in
  perpetuity. [cites: solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-1]

## References

- corpus entries (also in `derives_from`):
  - `solodit-cyfrin-2023-09-12-cyfrin-beanstalk-1-0` — static CHAIN_ID in domain separator → hard-fork replay (Medium)
  - `solodit-zokyo-2024-03-25-planar-finance-0-2` — missing nonce check in `permit` (Medium)
  - `solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-0-0` — nonce signed but never validated against stored value (Critical)
  - `solodit-cyfrin-2025-10-22-cyfrin-remora-dynamic-tokens-v2-1-0-1` — no nonce in struct hash → infinite reuse (Critical)
  - `solodit-zokyo-2024-02-26-tide-0-2` — chainId not validated → cross-chain replay (High)
  - `solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-0-2` — mutable token name breaks domain separator (Medium)
  - `solodit-cyfrin-2024-12-17-cyfrin-securitize-redeem-swap-vault-nav-v2-0-2-3` — static DOMAIN_SEPARATOR (Low)
  - `solodit-hexens-2025-02-10-train-protocol-2-0` — immutable DOMAIN_SEPARATOR invalid after hard fork (Low)
  - `solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-2-1` — replayable signature not bound to chain/instance (Low)
  - `solodit-zokyo-2024-07-01-heurist-3-1` — signature missing chainId/contract → cross-domain replay (Informational)
  - `solodit-zokyo-2024-06-07-zap-0-0` — airdrop signature reusable unlimited times (High)
  - `solodit-zokyo-2024-06-30-devve-0-3` — client-side staking signature reused to bypass UI invariants (High)
  - `solodit-zachobront-2023-04-15-hook-1-3` — `verifyingContract` set to wrong address (Medium)
  - `solodit-hexens-2024-09-19-stakewise-1-0` — `permit` front-running DoS (Low)
  - `solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-1-0` — `transferWithPermit` front-running DoS (Low)
  - `rekt-anyswap-rekt` — ECDSA `k` reuse → private-key recovery, $7.9M (Critical)
  - `rekt-trustedvolumes-rekt` — permissionless signer registration / unchecked signer authority, $5.87M (Critical)
  - `swc-133` — hash collisions with `abi.encodePacked` multiple variable-length args → signature bypass
