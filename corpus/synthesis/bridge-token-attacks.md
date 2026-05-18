---
id: synthesis-bridge-token-attacks
source: synthesis
source_url: null
title: "Token bridges (lock-mint / burn-mint): contract-level attack patterns, variants, audit checklist"
ingested_at: 2026-05-18T00:00:00Z
vuln_class:
  - bridge
  - cross-chain
  - access-control
  - accounting
  - validator-set
  - upgradeable-proxy
  - decimal-mismatch
  - fee-on-transfer
  - reorg
protocol_category:
  - bridge
  - cross-chain
  - messaging
  - layer-2
tags:
  - synthesis
  - bridge
  - lock-mint
  - burn-mint
  - token-bridge
  - validator-compromise
  - layerzero-peer
  - bridge-handler
  - reorg
derives_from:
  - rekt-nomad-rekt
  - rekt-wormhole-rekt
  - rekt-qubit-rekt
  - rekt-meter-rekt
  - rekt-polynetwork-rekt
  - rekt-ronin-rekt
  - rekt-roninnetwork-rektii
  - rekt-harmony-rekt
  - rekt-chainswap-rekt
  - rekt-griffinai-rekt
  - rekt-shibarium-rekt
  - rekt-shibarium-bridge-rekt
  - rekt-hyperbridge-rekt
  - solodit-zachobront-2023-06-01-alongside-1-1
  - solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-0-0
  - solodit-cyfrin-2024-05-24-cyfrin-linea-2-3
  - solodit-cyfrin-2024-05-24-cyfrin-linea-1-1
  - solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-1
  - solodit-hexens-2024-04-15-fuel-1-4
  - solodit-hexens-2024-04-15-fuel-0-0
  - solodit-hexens-2024-04-15-fuel-2-0
  - solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-1
  - solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-0-0
  - solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-0-0
  - solodit-zokyo-2024-10-24-beyond-1-2
  - solodit-auditone-2023-05-09-aurorafastbridge-0-0
  - arxiv-2601.12434
  - arxiv-2602.17805
---

# Token bridges (lock-mint / burn-mint): contract-level attack patterns

> Companion to [`synthesis-cross-chain-bridge-replay-and-signature-verification-flaws`](./cross-chain-bridge-replay-and-signature-verification-flaws.md), which focuses on signature/proof-verifier flaws. This note focuses on the **token-flow side** of the bridge — the handler/gateway logic that locks, burns, mints and releases assets, the validator/admin keys that authorise those flows, and the token-economics edge cases (decimals, fee-on-transfer, fake peers, refunds) that turn correct cryptography into incorrect accounting.

## Pattern

A canonical token bridge is two contracts and a trust layer:

1. **Source-chain gateway / lockbox** — accepts a `deposit(token, amount, dst)` (or `burn`) and emits an event or sends a message that the destination chain must observe.
2. **Destination-chain handler** — receives an attested message and `mint`s (or `release`s) the equivalent amount of the wrapped / canonical asset to the recipient.
3. **Attestation layer** — a multisig / MPC validator set, a light-client / merkle proof, a generic-message protocol (LayerZero peer, CCIP source, Wormhole VAA, IBC packet), or a zk proof.

The invariant the bridge must preserve is simple: **the amount minted on the destination chain must always be ≤ the amount actually escrowed (locked or burned) on the source chain, for the right token, by the right user, exactly once.** When this invariant is broken — even by a single missing check — the wrapped asset depegs immediately (Meter, Qubit, GriffinAI, Hyperbridge) and the bridge's TVL on the lock side is drained at the rate the destination liquidity pool can absorb (Wormhole, Nomad, Ronin).

Historically, this is the single largest source of systemic loss in DeFi: **>$2.8B since 2021 across token-bridge incidents** (arxiv-2601.12434), and four of the top five entries on the rekt.news leaderboard are token-bridge exploits (rekt-ronin-rekt, rekt-polynetwork-rekt, rekt-wormhole-rekt, rekt-nomad-rekt). The reason is structural: the bridge holds pooled collateral for many users and many chains, mints unbacked supply with one wrong message, and has no graceful failure mode between "fully operational" and "catastrophically compromised" (arxiv-2601.12434 frames this as the *binary failure mode* that motivates Contained-Degradation designs).

In practice, the bugs cluster into three layers — (a) **attestation layer compromise** (validator keys, trusted peers, low thresholds), (b) **handler/accounting logic flaws on either side of the bridge** (wrong-token, decimals, fee-on-transfer, double-spend, stuck funds), and (c) **upgrade/admin abuse** (initialiser skipped, REMOTE_TOKEN swap, storage-slot collision). The replay/signature-verifier family is treated in the companion synthesis; everything else lives below.

## Variants

### V1: Handler accepts deposit for a "free" or wrong token (deposit path)

The source-chain `deposit` function does not bind the *thing actually transferred* to the *thing credited on the destination chain*. The most common forms:

* **Zero-address pseudo-token / dead code path.** Qubit Finance ($80M, rekt-qubit-rekt): the legacy `QBridge.deposit()` function was kept after `depositETH` was added, and `tokenAddress.safeTransferFrom(depositer, address(this), amount)` does **not revert when `tokenAddress` is the zero address**. The attacker called the legacy `deposit()` with `tokenAddress = 0` and an arbitrary `amount`, the transfer was a no-op, and the bridge credited the attacker with 77,162 qXETH on BSC (~$185M of borrow collateral) against zero locked ETH on mainnet. Pattern: any deposit function that supports both ERC-20 and "ETH" via a zero-address sentinel is dangerous if the ERC-20 path isn't gated against `tokenAddress == address(0)`.

* **Wrapped-native shortcut.** Meter.io ($4.4M, rekt-meter-rekt): a fork of ChainSafe's ChainBridge added an optimization — "if the token being bridged is wrapped native, don't burn/lock since the wrapped native is already unwrapped and transferred to the handler". The `depositEth` variant asserted `msg.value == amount`, but the unguarded `deposit(token, amount, calldata)` did not — so the attacker called `deposit` with arbitrary `amount` calldata, no actual transfer occurred, and the bridge minted ~$4.4M of BNB+wETH on BSC. The collateral damage hit Hundred Finance for an additional $3.3M because their lending market priced BNB.bsc from the depegged Meter bridge.

* **Compromised admin re-points the "trusted peer" of the bridge.** GriffinAI ($3M, rekt-griffinai-rekt): an admin key was used to call `setPeer` on Griffin AI's LayerZero OFT, designating a freshly deployed fake ERC-20 (`0x7a8caf…`) on Ethereum as the trusted source. The bridge then accepted "deposits" of the fake token and minted 5B real $GAIN on BNB Chain — five times the intended total supply. Same playbook (mis-set LayerZero peer) was used against Seedify and Yala earlier.

### V2: Lock-side collateral drift (fee-on-transfer / rebasing / decimals)

Even when the message is authentic, the *recorded* amount can diverge from the *received* amount, leaving the bridge perpetually under-collateralised.

* **Fee-on-transfer.** Fuel's `FuelERC20GatewayV4.deposit` (Hexens, solodit-hexens-2024-04-15-fuel-1-4): `safeTransferFrom(msg.sender, this, amount)` is followed by minting `amount` on the L2, but for fee-on-transfer tokens the contract received less. A second user requesting withdrawal will either fail or consume another user's collateral. The fix is the canonical `balanceBefore` / `balanceAfter` diff to mint only what was actually received.

* **Decimal mismatch — bridged vs. native.** Linea TokenBridge (solodit-cyfrin-2024-05-24-cyfrin-linea-2-3): `_safeDecimals` defaults to 18 when `decimals()` reverts. A native token with, say, 6 decimals bridges over with 18 decimals on the destination chain; when the user burns to bridge back, the `transfer` either reverts (native has <18 decimals) or sends the user a tiny fraction of what they bridged (native has >18 decimals). Recommended fix: revert in `_safeDecimals` when no decimals are returned.

* **Decimal mismatch — same logical asset on different chains.** Wormhole CCTP integration (solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-1): USDC has 6 decimals on Ethereum but 18 on BNB Chain. Burning 20 USDC encoded as `20e18` on BNB Chain and minting on Ethereum gives the recipient `20e12 = 20,000,000,000,000` USDC. Fuel's bridge had the same shape (solodit-hexens-2024-04-15-fuel-0-0): the Sway side hard-coded 9 decimals for all bridged assets, but the EVM gateway adjusted by source decimals — bridging USDC produced a 1000× *smaller* mint on Fuel because the divisor was applied on the EVM side but not re-applied on the Fuel side.

### V3: Mint-side handler accepts unauthenticated messages

The destination-chain `_receive` / `claim` / `process` function does not authenticate that the message came from a trusted source on the source chain.

* **CCIP message without sender validation.** YieldFi (solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-0-0): `BridgeCCIP._ccipReceive` decoded `Any2EVMMessage.data`, checked `processedMessages[_hash]`, and minted/unlocked yield tokens — but never verified `any2EvmMessage.sender` against a list of trusted peers per source chain. Any address on any CCIP-supported chain could craft a message and drain the bridge or mint unlimited tokens on L2. Pattern: when integrating CCIP / LayerZero / Wormhole / IBC, the per-source-chain *peer allow-list* is a separate, mandatory check on top of the generic-messaging protocol's own auth.

* **Unvalidated CPI target (Solana / SVM).** Securitize on/off-ramp (solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-0-0): the swap process pulled the `rwa_rbac` program account from user-supplied `remaining_accounts` and CPI'd into it with the on-ramp authority as signer, *without* validating that `additional_accounts[0]` was the real RBAC program. An investor could swap 10 USDC, point the bridge at a malicious clone of `rwa_rbac` that re-encodes the CPI data with `amount = u64::MAX`, and mint effectively infinite DsTokens. Equivalent EVM mistake: accepting an attacker-supplied `address` and calling it with privileged state.

* **EthCrossChainManager-as-arbitrary-caller.** Poly Network ($611M, rekt-polynetwork-rekt): `verifyHeaderAndExecuteTx` validated the merkle proof but then `executeCrossChainTx` called any target with the manager's privileges. The attacker brute-forced a 4-byte selector collision and made the manager call `putCurEpochConPubKeyBytes` on its own data contract, rotating the validator keys to attacker-controlled values. Lesson, in the auditor's words: *"if you have cross-chain relay contracts like this, MAKE SURE THEY CAN'T BE USED TO CALL SPECIAL CONTRACTS. Separate concerns."*

* **VAA / proof-verifier bug.** Wormhole ($326M, rekt-wormhole-rekt): a Solana sysvar/precompile mismatch let `verify_signatures` accept a `SignatureSet` constructed in a prior transaction with only 0.1 ETH at risk; the attacker then minted 120k whETH on Solana against zero locked ETH on Ethereum. Hyperbridge ($2.5M, rekt-hyperbridge-rekt): the custom `MerkleMountainRange.CalculateRoot()` had no `require(leaf_index < leafCount)` bounds check, so a forged proof where `leaf_index=1, leafCount=1, proof[0]=expected_root` caused the function to return `proof[0]` and accept any message; the attacker became admin of the bridged DOT token and minted 1B DOT. *(Cross-reference with the replay/verifier synthesis; these are listed here because the impact reduces directly to "mint unbacked tokens.")*

### V4: Validator / multisig / MPC compromise (attestation-layer keys)

When proof verification *is* sound, the cheapest attack is to take over the signers.

* **Low-threshold multisig.** Ronin I ($624M, rekt-ronin-rekt): 5-of-9 validator signature threshold, four of those nine operated by Sky Mavis. A months-old whitelist from Axie DAO was never revoked, letting the attacker reach the fifth signature with only Sky Mavis's keys plus that single legacy delegation. Harmony Horizon ($100M, rekt-harmony-rekt): 2-of-5 multisig with hot-wallet keys (suspected plaintext); two key compromises drain the entire bridge.

* **Flash-loaned validator power.** Shibarium ($3M, rekt-shibarium-rekt): bridge security depended on 8-of-12 validator signatures, but voting power was bought with a same-block flash loan of 4.6M BONE; the attacker delegated, signed a fraudulent checkpoint, and unwound the loan with the proceeds. L2BEAT had flagged this exact scenario *before* the attack. Lesson: validator power must be checkpoint-stable, not spot-purchasable inside a single block/epoch.

* **MEV-bot front-running a half-initialised V3 bridge.** Ronin II ($12M, rekt-roninnetwork-rektii): the V3→V4 upgrade called `initializeV4` but skipped `initializeV3`, leaving `_totalOperatorWeight = 0`, which made `minimumVoteWeight` effectively zero — *no signatures required at all* to authorize withdrawals. An MEV bot spotted it first and walked off with $12M before the team noticed.

### V5: Upgrade / initialiser bugs in the bridge contract itself

The bridge code is correct; the deployment / upgrade is not.

* **Trusted-root-set-to-zero after upgrade.** Nomad ($190M, rekt-nomad-rekt): the upgraded `Replica` contract registered the zero message-hash as a trusted Merkle root. `process()`'s `require(roots[messageHash] != 0)` check now passed by default for any payload, since unset `roots[…]` was also `0x00…00`. The exploit was copy-pasteable from Etherscan, leading to a 100+ address crowd-hack. Quantstamp had flagged a similar issue (`QSP-19`) in the pre-upgrade audit and the team had dismissed it.

* **Storage-layout shift on upgrade re-opens `initialize`.** Linea L1 TokenBridge ($29M at risk, solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-0-0): replacing OZ `ReentrancyGuardUpgradeable` with a custom transient-storage version dropped `Initializable` from the inheritance chain. The initialisation flag (slot 0) became a gap and slot 50 became the new init flag — but slot 50 was zero, so post-upgrade *any* address could call `TokenBridge.initialize`, grant itself `SET_MESSAGE_SERVICE_ROLE`, set a malicious message service, and `completeBridging` to drain every locked ERC-20. Mitigation: storage-layout diff on every upgrade *and* `reinitializer`-wipe of slots that change semantic meaning.

* **Owner-tunable bridge config can be weaponised against locked funds.** Alongside `BridgedIndexToken.setBridge()` (solodit-zachobront-2023-06-01-alongside-1-1): the L1 token's `REMOTE_TOKEN` value (checked by Optimism's StandardBridge before minting on L1) was a freely settable owner variable. A malicious owner can deploy a fake L2 token, deposit it through the L2 bridge, change `REMOTE_TOKEN` to point at the fake during the 7-day window, withdraw legitimate funds on L1, then revert the change. The fix: lock the two-address config to a one-time setter or make them immutable.

* **`bridgeBurn` allows burning anyone's balance.** STBL_USST (solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-1): `bridgeBurn(address _from, uint256 _amt)` lets the `BRIDGE_ROLE` `_burn(_from, _amt)` for *any* user without approval. A bridge-contract compromise (V4) becomes a single-tx mass burn of every holder's tokens. The safer pattern: `_burn(msg.sender, _amt)` — the bridge must already hold the tokens, so the user actively transferred-in first.

### V6: Signer-registry replay / sloppy auth (legacy multisig variant)

ChainSwap ($4.4M, rekt-chainswap-rekt): the proxy factory on Ethereum minted tokens directly into the supplied target address with a "sloppy auth check" that accepted a *new* address as the signature each call — i.e. the signer registry treated first-seen addresses as valid signers. The attacker minted 500k WILD per call ×40 and bridged out to BSC. Lesson: any auth scheme that *expands* the trusted set on use, rather than gating against a fixed registry, is broken.

### V7: Reorg-based double-spend on probabilistic finality

AuditOne / Aurora Fast Bridge (solodit-auditone-2023-05-09-aurorafastbridge-0-0): the bridge processed source-chain events before the source chain had reached finality. A short-range reorg lets the attacker get the destination-side credit *and* keep the source-side balance after the deposit transaction is dropped. Fix: wait `k`-confirmations sized to the source chain's reorg-depth distribution (Bitcoin/PoW chains: dozens; Ethereum post-Merge: 64–128 slots / finalized blocks; Polygon: many more).

### V8: Non-unique events / messages enabling replay on the receiver

Zokyo / Beyond (solodit-zokyo-2024-10-24-beyond-1-2): `OriginalTokenBridge.unwrapBTC` emits `UnwrapBTC(to, amount, referralCode)` with **no unique identifier**. If the off-chain relayer or destination contract dedupes by event hash and two unwraps coincidentally use the same `(to, amount, referralCode)`, only one is recorded; if it dedupes by tx hash but reads the event twice for any reason, the user is credited twice. Mitigation: include a monotonically increasing nonce (per-user or per-bridge) in every cross-chain event, and key the destination's processed-set on it.

### V9: Stuck / unrefundable funds (claim-side liveness)

Even if the mint side rejects an invalid message, money locked on the source side must always be recoverable. Two recurring shapes:

* **Failing destination call with no source-side cancel.** Linea L1↔L2 messaging (solodit-cyfrin-2024-05-24-cyfrin-linea-1-1): the bridge's last step is `claimMessage` / `claimMessageWithProof` doing an arbitrary call with arbitrary calldata; if that call reverts, the user can retry forever but cannot cancel or refund on the source chain. Bridge teams underestimate this risk because the funds aren't *stolen* — they're stuck.

* **Failed deposit with no refund register.** Fuel sway bridge (solodit-hexens-2024-04-15-fuel-2-0): most failure paths call `register_refund` so the user can later claim, but the contract-callback path does not — if the destination contract reverts, no refund was registered and the assets are permanently lost in the gateway.

* **L2 stops producing blocks.** Shibarium I ($2.6M stuck, rekt-shibarium-bridge-rekt): users deposited ETH/BONE into the L1 bridge while the L2 chain halted; withdrawals can't be initiated from L2 because there are no L2 blocks. Recoverable here only because the bridge was an upgradeable proxy with a known owner.

* **Expired guardian set traps in-flight VAAs.** Wormhole CCTP (companion synthesis V10): if the source-side burn happens under guardian set `N` but the destination-side mint isn't claimed before set `N` expires (24h), the message dies, the source tokens stay burned, and the user gets nothing. Bridge contracts that hard-expire signed artifacts must also expose a refund path.

### V10: Owner / `BRIDGE_ROLE` centralisation (rug primitives)

Closely related to V4 but distinct: even a non-compromised admin role can drain the bridge by design if scope is too broad.

* `BRIDGE_ROLE` may burn from arbitrary addresses (STBL_USST, V5 / solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-1).
* `releaseRewardForRelayer(amount)` with no upper bound (solodit-zokyo-2024-02-27-interplanetary-consensus-ipc-0-1) — registered subnets can withdraw arbitrary ETH from the IPC Gateway.
* Owner can swap `REMOTE_TOKEN` mid-flight (V5 / Alongside).
* Single-EOA bridge admin (rekt-griffinai-rekt) → fake peer + arbitrary mint.

These collapse to: any privileged role on a bridge that holds pooled liquidity should be (a) a high-threshold multisig with timelock, (b) scoped to specific tokens/amounts, and (c) covered by monitoring alerts and an automatic pause.

### V11: Intent-/solver-based bridges — liquidity exhaustion

arxiv-2602.17805 ("Exploiting Liquidity Exhaustion Attacks in Intent-Based Cross-Chain Bridges"): the newer wave of bridges (Across, deBridge, Mayan Swift) replaces lock-mint with off-chain solvers fronting liquidity for users. The systemic risk shifts from "validator compromise" to **solver liquidity concentration + delayed settlement**. Across 3.5M intents ($9.24B over 5 months), 80.5% of attacks against deBridge under current parameters were profitable, with a mean attack profit of $286 and Byzantine variants able to suppress availability across all three protocols (~$978 of solver loss roughly every 16 minutes). Audit implication: intent-based bridge contracts must be modelled for griefing/exhaustion under rational *and* Byzantine solver behaviour, not just for "is the message valid".

## Audit checklist

For every bridge handler / gateway / token-pair in scope, work down this list:

**Deposit path (lock or burn side):**

- Is there exactly one canonical deposit function per supported token type, or are there multiple deposit functions where one of them skips a critical check (Qubit's `deposit` vs `depositETH`, Meter's `deposit` vs `depositEth`)?
- Does the deposit function revert if `tokenAddress == address(0)` (or whatever the native-asset sentinel is) when called via the ERC-20 path?
- Does the deposit function gate native-asset deposits on `msg.value == amount`?
- For ERC-20 deposits, is the credited amount computed from `balanceAfter - balanceBefore` rather than the `amount` argument, so that fee-on-transfer/rebasing tokens cannot drift the lock balance?
- Are decimals captured *from the source token at deposit time* and passed through to the destination, rather than defaulting to 18 (or any constant)?
- For ETH bridges built on `payable` plus `receive()` fallback, can a user send ETH via `receive()` and bypass the deposit accounting entirely (Symbiosis Wrapper pattern)?
- If a deposit triggers a custom callback / `process_message`, is a refund pre-registered before the external call and only cleared on success?

**Attestation / message layer:**

- Does the destination handler verify *both* (a) the generic messaging protocol's auth (CCIP / LayerZero / Wormhole / IBC self-checks) *and* (b) an application-level allow-list of `(sourceChainSelector, sourcePeerAddress)`? Missing (b) is the YieldFi-class bug.
- For Solana/SVM bridges: is every program account in `remaining_accounts` validated against the expected program ID before any signed CPI?
- For LayerZero OFTs: who can call `setPeer`? Is it timelocked? Is there an off-chain alert on peer changes? GriffinAI/Seedify/Yala all turned on a `setPeer` change.
- Does the destination handler restrict *what target contracts* it can dispatch to? Specifically, the messaging dispatcher must not be the *owner* of any contract whose state it can call (Poly Network rule).
- Is the merkle/MMR/IAVL proof verifier independently audited (specialist Solidity review) *and* fuzz-tested with malformed inputs, including `leaf_index >= leafCount`, single-leaf trees, empty proofs, and root==proof[0] degenerate cases?

**Validator / signer set:**

- What is the signing threshold, who controls each key, and how diverse is custody? (Ronin I: four-of-nine keys at the same operator.)
- Can voting power be acquired and exercised within the same block via flash loan / same-block stake (Shibarium)?
- Are validator keys hot-wallet / plaintext (Harmony) or in HSM/MPC?
- Is there a rotation / whitelist that must be re-confirmed periodically? Lingering one-off delegations are how Ronin I's fifth key was reached.

**Upgradeability:**

- Diff the storage layout (`forge inspect ... storageLayout`) of the pre- and post-upgrade implementations. Has any state slot changed semantic role? Has the `Initializable` flag's slot moved? (Linea TokenBridge $29M case.)
- After upgrade, can `initialize` be called by a permissionless attacker? Has every `initializeVN` been invoked, or is the latest re-init dependent on a previous one having run (Ronin II)?
- Are all trusted-root / threshold-weight / merkle-mountain-range starting values explicitly set in the upgrade tx, with a regression test that asserts they are *non-zero* before traffic resumes (Nomad)?

**Admin / role surface:**

- Can `BRIDGE_ROLE` burn from arbitrary holders without their approval (STBL_USST)? Prefer `_burn(msg.sender, _amt)` semantics where the bridge actively pulls tokens.
- Is `REMOTE_TOKEN` / peer-token configuration owner-tunable post-deployment? If yes, can it be tightened to a one-time setter or governed by a long timelock?
- Are reward/withdraw helper functions (`releaseRewardForRelayer`, `emergencyWithdraw`, `sweep`) bounded by per-call and per-epoch caps?
- Is there a withdrawal-rate limit per token + per address per day that would have capped Ronin II's $12M loss? (Ronin's daily limit is what *prevented* a worse outcome.)

**Token-flow accounting:**

- Are unique nonces / event IDs in every cross-chain event so the receiver can dedup deterministically (Beyond)?
- Is the message processed-set keyed on the event nonce, not just `keccak(eventData)`?
- Does the source chain wait for adequate finality before the destination side acts on its events (Aurora Fast Bridge / V7)? What's the configured `k`-confirmations and does it match the chain's actual reorg-depth distribution?
- For each `(source-chain decimals, destination-chain decimals)` pair, is there a decimal-adjustment routine, *applied on exactly one side*, with explicit revert on non-integer remainder?

**Liveness / refund:**

- If the destination call reverts, can the user retry indefinitely *and* cancel/refund on the source side?
- If the destination chain halts (Shibarium I), is there a documented recovery path (proxy upgrade, owner-controlled drain, etc.)?
- If signed artifacts have a TTL (Wormhole guardian-set expiry), is there a refund path for in-flight messages that miss the window?

**Intent / solver bridges:**

- Are solver inventories monitored for concentration (a few solvers carrying >50% of flow are a single point of failure)?
- Does the contract handle Byzantine solver behaviour — repeated reverts, race conditions, claim front-runs — without locking user funds or amplifying solver losses (arxiv-2602.17805)?

## Prior incidents

- **Poly Network (Aug 2021) — $611M**: `EthCrossChainManager` could be tricked into calling its own `EthCrossChainData` contract via a brute-forced 4-byte sighash collision, letting the attacker rotate validator public keys without any signature compromise [cites: rekt-polynetwork-rekt].
- **ChainSwap (Jul 2021) — $4.4M**: per-tx auth accepted a new address as the signature each call; 20 tokens minted across BSC [cites: rekt-chainswap-rekt].
- **Wormhole (Feb 2022) — $326M**: Solana `verify_signatures` precompile mismatch let a `SignatureSet` from a previous tx be reused to mint 120k whETH unbacked [cites: rekt-wormhole-rekt].
- **Qubit (Jan 2022) — $80M**: dead `deposit(tokenAddress=0, amount=...)` path on the QBridge handler credited xETH on BSC without any ETH ever locked [cites: rekt-qubit-rekt].
- **Meter (Feb 2022) — $4.4M (+ $3.3M collateral damage to Hundred Finance)**: wrapped-native shortcut in the deposit handler didn't enforce `msg.value == amount` [cites: rekt-meter-rekt].
- **Ronin I (Mar 2022) — $624M**: 5-of-9 multisig with four keys at one operator and a one-month-old delegation that was never revoked [cites: rekt-ronin-rekt].
- **Harmony Horizon (Jun 2022) — $100M**: 2-of-5 multisig with suspected plaintext hot-wallet keys [cites: rekt-harmony-rekt].
- **Nomad (Aug 2022) — $190M**: post-upgrade Replica trusted the zero hash as a merkle root; every `process()` call succeeded by default and the exploit was copy-pasteable [cites: rekt-nomad-rekt].
- **Shibarium I (Aug 2023) — $2.6M stuck**: L2 halted, no withdrawal path from the L2 side; recoverable only via proxy upgrade [cites: rekt-shibarium-bridge-rekt].
- **Ronin II (Aug 2024) — $12M**: `initializeV3` skipped during V3→V4 upgrade, leaving `_totalOperatorWeight = 0` and disabling `minimumVoteWeight`; MEV white-hat returned funds [cites: rekt-roninnetwork-rektii].
- **Shibarium II (Sep 2025) — $3M**: flash-loaned 4.6M BONE bought temporary control of 10-of-12 validators in a single block; bridge approved a fraudulent checkpoint and drained itself. L2BEAT had warned about this exact scenario [cites: rekt-shibarium-rekt].
- **GriffinAI (Sep 2025) — $3M (+ 4.85B phantom tokens still unsold)**: compromised admin called `setPeer` to designate a fake ERC-20 as the LayerZero peer; bridge minted 5B unbacked $GAIN; dump caused -90% price [cites: rekt-griffinai-rekt].
- **Hyperbridge (Apr 2026) — $2.5M**: custom `MerkleMountainRange.CalculateRoot()` library missed a `require(leaf_index < leafCount)` bounds check; forged proof made attacker admin of the bridged DOT token contract and minted 1B DOT. Pre-audit had explicitly recommended specialist Solidity review of the custom libraries [cites: rekt-hyperbridge-rekt].

## References

The full corpus entries underlying this synthesis (also listed in `derives_from`):

* rekt-nomad-rekt — $190M, post-upgrade zero-root accepted as trusted
* rekt-wormhole-rekt — $326M, Solana `verify_signatures` bypass
* rekt-qubit-rekt — $80M, zero-address deposit path
* rekt-meter-rekt — $4.4M, wrapped-native handler `amount`-not-checked
* rekt-polynetwork-rekt — $611M, sighash-collision into self-privileged contract
* rekt-ronin-rekt — $624M, 5-of-9 validator-key compromise
* rekt-roninnetwork-rektii — $12M, missed `initializeV3` upgrade
* rekt-harmony-rekt — $100M, 2-of-5 multisig with hot keys
* rekt-chainswap-rekt — $4.4M, signer-registry replay
* rekt-griffinai-rekt — $3M, malicious `setPeer` on LayerZero OFT
* rekt-shibarium-rekt — $3M, flash-loaned 10-of-12 validator capture
* rekt-shibarium-bridge-rekt — $2.6M stuck, halted L2 with no withdrawal path
* rekt-hyperbridge-rekt — $2.5M, MMR `CalculateRoot` missing bounds check
* solodit-zachobront-2023-06-01-alongside-1-1 — owner can swap `REMOTE_TOKEN` (Medium)
* solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-0-0 — storage-slot shift re-opens `initialize` ($29M at risk, Critical)
* solodit-cyfrin-2024-05-24-cyfrin-linea-2-3 — `_safeDecimals` defaults to 18, decimal mismatch (Low)
* solodit-cyfrin-2024-05-24-cyfrin-linea-1-1 — no cancel/refund when destination call reverts (Medium)
* solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-1 — CCTP cross-domain decimal mismatch (Informational)
* solodit-hexens-2024-04-15-fuel-1-4 — FoT tokens drift the Fuel ERC20 gateway balance (Medium)
* solodit-hexens-2024-04-15-fuel-0-0 — decimal hard-coded to 9 on Sway side, no metadata pass-through (High)
* solodit-hexens-2024-04-15-fuel-2-0 — failed contract callback path doesn't register refund (Low)
* solodit-cyfrin-2025-09-05-cyfrin-stbl-v2-0-0-1 — `bridgeBurn(_from, _amt)` allows arbitrary holder burn (Medium)
* solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-0-0 — CCIP `_ccipReceive` missing source-peer validation (High)
* solodit-cyfrin-2026-02-19-cyfrin-securitize-svm-on-off-ramp-v2-0-0-0 — unvalidated `rwa_rbac` program in CPI; mint DsTokens out of thin air (Critical)
* solodit-zokyo-2024-10-24-beyond-1-2 — `UnwrapBTC` event lacks unique id, double-spend risk (Medium)
* solodit-auditone-2023-05-09-aurorafastbridge-0-0 — block reorg enables double-spend without finality wait (High)
* arxiv-2601.12434 — ASAS-BridgeAMM; framing of bridges as the single largest systemic DeFi risk vector ($2.8B since 2021); Contained-Degradation design
* arxiv-2602.17805 — Liquidity-exhaustion attacks on intent-based bridges (Mayan Swift, Across, deBridge) over $9.24B of historical flow
