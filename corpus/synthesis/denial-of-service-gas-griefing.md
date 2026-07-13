---
id: synthesis-denial-of-service-gas-griefing
source: synthesis
source_url: null
title: "Denial of Service & Gas Griefing: pattern, variants, audit checklist"
ingested_at: 2026-06-04T20:18:54Z
vuln_class:
  - dos
  - gas-limit
  - unbounded-loop
  - gas-griefing
  - external-call
  - push-payment
protocol_category:
  - defi
  - staking
  - governance
  - amm
  - infrastructure
tags:
  - synthesis
  - denial-of-service
  - gas-griefing
  - dos
derives_from:
  - swc-128
  - solodit-zokyo-2024-11-19-tren-0-0
  - solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5
  - solodit-auditone-2022-12-14-unicrow-0-3
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2
  - solodit-pashov-audit-group-2022-11-01-zerem-1-2
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0
  - solodit-zokyo-2023-08-11-velocore-0-1
  - solodit-zokyo-2024-02-26-tide-0-1
  - solodit-guardian-audits-2022-10-24-gmx-1-1
  - solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2
  - solodit-hexens-2023-04-14-lido-0-3
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0
  - arxiv-2604.21169
---

# Denial of Service & Gas Griefing

## Pattern

Denial-of-Service (DoS) bugs in smart contracts are cases where an attacker
(or even an unlucky participant) can permanently or temporarily block a
function that *should* be callable, without necessarily stealing anything.
Because every EVM transaction is bounded by the block gas limit, any
operation whose cost grows with attacker-influenced state, or whose success
depends on an external party cooperating, is a candidate. The core question
an auditor asks is: *"Can someone make this function impossible (or
uneconomical) to execute for everyone else?"* The damage ranges from
griefing (wasted gas, delayed execution) to hard liveness failures where
user funds are frozen because the only withdrawal/settlement path reverts.

The most classic instance is the **unbounded loop**: a function iterates
over an array or list that grows over time, and once it is large enough the
loop's gas cost exceeds the block gas limit, so the call can never succeed
again (swc-128, solodit-zokyo-2024-11-19-tren-0-0,
solodit-guardian-audits-2022-10-24-gmx-1-1). A close cousin is the
**poisoned queue/list**: the data structure isn't naturally unbounded, but
an attacker can cheaply spam entries (zero-value requests, dust orders) to
inflate an O(n) operation until it bricks (solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2,
solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5).

The second large family is the **failing external call**. When a contract
*pushes* value (ETH or tokens) to a recipient and reverts the whole flow on
failure, any single hostile or non-cooperating recipient can wedge a
multi-party settlement, a FIFO queue, or a batch (solodit-auditone-2022-12-14-unicrow-0-3,
solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0,
solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2,
solodit-zokyo-2023-08-11-velocore-0-1). A subtler variant is **gas
griefing**: even when the caller checks only `success`, Solidity copies the
callee's returned bytes into memory, so a recipient that returns a huge
payload ("return bomb") forces the caller to pay for memory expansion and
can trigger out-of-gas (solodit-pashov-audit-group-2022-11-01-zerem-1-2,
solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0,
solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13).

Finally, DoS can come from **environmental manipulation**: forcing a
strict balance/equality check to fail by force-feeding ETH
(solodit-hexens-2023-04-14-lido-0-3), front-running with a deliberately
under-gassed relayed call to burn a nonce (solodit-zokyo-2024-02-26-tide-0-1),
abusing new EVM features so that "EOA" recipients suddenly run callbacks
that consume nearly all forwarded gas (solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0),
or — at the infrastructure layer — crafting inter-transaction state
dependencies that deny multi-round block-building simulation
(arxiv-2604.21169). The unifying theme: control flow or cost is exposed to
an adversary who pays little and forces everyone else to pay too much or to
fail outright.

## Variants

### V1: Unbounded loop hitting the block gas limit

A function loops over an array/mapping-list whose size grows monotonically
and is never capped. Once big enough, the call costs more than the block
gas limit and is permanently bricked. In Tren's `massUpdateRewards` the
loop walks every investment ID in a pool, and `removeIdFromList` has the
same shape (solodit-zokyo-2024-11-19-tren-0-0). GMX's `setPrices` loops
over unbounded `tokens`/`signers`/`prices` arrays with memory-expansion
costs compounding for long swap routes (solodit-guardian-audits-2022-10-24-gmx-1-1).
swc-128 is the canonical write-up and notes that even *clearing* a large
array can blow the limit. Fixes: cap the array length, paginate across
multiple transactions, or restructure so no full-array iteration is needed.

### V2: Queue / list poisoning via cheap spam (O(n) amplification)

Here the structure isn't inherently unbounded, but entry cost is far lower
than the per-element processing cost, so an attacker inflates it on purpose.
Casimir's `requestUnstake()` accepted `amount = 0`, letting an attacker
balloon a FIFO unstake queue whose `remove()` is O(n) until `fulfillUnstake()`
exceeds the block gas limit (solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2).
In the Uniswap-v3 limit-order registry, `performUpkeep` walks the order
list until it finds an order matching the walk direction; an attacker
places many cheap opposite-direction orders so the walk consumes more than
the per-upkeep gas budget, blocking fulfillment of legitimate in-the-money
orders (solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5).
Fixes: enforce a meaningful minimum (stake/order size), or split the data
structure so processing doesn't traverse attacker-controlled entries.

### V3: Push-payment revert DoS (one bad recipient blocks everyone)

A contract pushes funds and treats a failed transfer as a fatal revert, so
any recipient can grief the entire operation by reverting in `receive()`/
`fallback()`, or by being a blacklisted token holder. Unicrow's escrow used
a push pattern, so any party (buyer/seller/marketplace) could reject funds
(reverting contract or ERC777 hook) and prevent settlement
(solodit-auditone-2022-12-14-unicrow-0-3). Casimir's `fulfillUnstake()`
reverted on a failed low-level ETH send, and because the queue is FIFO one
attacker reverting on `receive()` froze *all* unstakes
(solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0). OctoDefi's fee handler
called `safeTransferFrom`/`transfer` to multiple recipients in one path, so
a USDT/USDC-blacklisted or reverting `creator` bricked all future
automation (solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2). Velocore's
vault settled many token transfers atomically, so one externally-griefed
transfer reverted a 20-operation batch (solodit-zokyo-2023-08-11-velocore-0-1).
Canonical fix: **pull-over-push** — credit balances and let each party
withdraw separately; or isolate each transfer in try/catch so one failure
doesn't revert the rest.

### V4: Gas griefing via returned data / return bombs

Even a "fire and forget" call like `(bool ok, ) = target.call{value:..}("")`
still copies the callee's return data into memory; a malicious callee that
returns a giant byte array forces the caller to pay for memory expansion,
griefing a relayer or causing out-of-gas. Zerem's relayer-paid ETH transfer
was exposed exactly this way, fixed by an assembly `call` that ignores
return data (solodit-pashov-audit-group-2022-11-01-zerem-1-2); Thermae had
the same low-level-call recommendation and pointed to `ExcessivelySafeCall`
(solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0). DeXe escalated this into a
governance attack: `GovPool::execute` did low-level calls to untrusted
action executors without bounding `returnedData`, so a proposal author
could craft an executor that returns empty bytes when the vote passes but a
**return bomb** when it fails — guaranteeing one-sided execution where
`actionsAgainst` can never run (solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13).
Fix: use low-level/assembly calls that don't copy return data, or cap copied
return bytes.

### V5: Forced-state / strict-check DoS (force-feeding & strict equality)

Contracts that assert exact balances or strict equalities can be bricked by
an attacker who manipulates the environment. In Lido, `deposit` computed
`unaccountedEth` without counting the StakingRouter's balance; an attacker
`selfdestruct`-ed ETH into the StakingRouter so that dust returned to Lido
made a later assertion fail, reverting `deposit`
(solodit-hexens-2023-04-14-lido-0-3). Because ETH can be force-sent
(`selfdestruct`, and `sendall` post-EIP-4758), any logic of the form
`require(address(this).balance == expected)` is DoS-prone. Fix: track
accounting in storage rather than reading raw balances, and avoid strict
equality on values an attacker can nudge.

### V6: Caller-controlled / relay gas & block-building DoS

When a function lets the caller specify the gas forwarded to a sub-call
without enforcing a minimum, an attacker can front-run a relayed/forwarded
transaction with a higher gas price but deliberately insufficient gas: the
attacker's tx fails yet consumes the victim's nonce, blocking the intended
transaction (solodit-zokyo-2024-02-26-tide-0-1). Fix: enforce a minimum gas
requirement (with a buffer for ETH transfers) inside the forwarder. At the
infrastructure layer, the same liveness concern applies to block building:
multi-round transaction simulation can be denied by crafting inter-
transaction dependencies in smart-contract state that break cross-round
consistency assumptions (arxiv-2604.21169).

### V7: Unbounded gas forwarded to recipient callbacks (modern EVM twist)

Token-standard callbacks (`onERC1155Received`, ERC777 hooks) forward most of
the remaining gas to the recipient. Historically EOAs skipped the callback
(`to.code.length == 0`), but with EIP-7702 an EOA can install a delegation
designator so `to.code.length > 0`, triggering the acceptance check and
handing the recipient ~`(63/64)^2 ≈ 96.9%` of remaining gas. In Myriad's
CLOB, `matchCrossMarketOrders` loops calling `safeTransferFrom`, so an
attacker at index 0 receives the callback first and burns enough gas to
starve settlement for everyone after them — operator-paid griefing
(solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0). Fix: cap forwarded
gas to callbacks, use pull distribution, or avoid in-loop callback-bearing
transfers.

## Audit checklist

- Does any function loop over an array/list whose length grows over time and
  is not capped? (swc-128, solodit-zokyo-2024-11-19-tren-0-0,
  solodit-guardian-audits-2022-10-24-gmx-1-1)
- Can an attacker cheaply add entries (zero/dust amounts, spam orders) to a
  data structure that is later iterated with O(n) cost? Is there a minimum
  size/stake requirement to make spamming uneconomical?
  (solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2,
  solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5)
- Is there a clearing/cleanup path that itself iterates a large array and
  could exceed the gas limit? (swc-128)
- Does the contract *push* ETH/tokens and revert the whole flow on a single
  failed transfer? Could one reverting recipient block a queue, batch, or
  multi-party settlement? (solodit-auditone-2022-12-14-unicrow-0-3,
  solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0,
  solodit-zokyo-2023-08-11-velocore-0-1)
- Is the protocol using a **pull-over-push** withdrawal pattern where it
  matters, or are transfers isolated in try/catch so one failure doesn't
  revert the rest? (solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0,
  solodit-zokyo-2023-08-11-velocore-0-1)
- Could a blacklistable token (USDC/USDT) or a reverting `receive()` on any
  fee/payout recipient brick a shared code path for all users?
  (solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2)
- Are external calls written so returned data is copied to memory
  (`(bool ok, ) = x.call(...)`) where a return bomb could grief gas? Should
  it use assembly/low-level call or `ExcessivelySafeCall`?
  (solodit-pashov-audit-group-2022-11-01-zerem-1-2,
  solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0)
- For calls to untrusted executors (governance, plugins), is copied return
  data bounded so a return bomb can't force one-sided/permanent DoS?
  (solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13)
- Does any logic use strict equality on `address(this).balance` or similar
  values an attacker can perturb via force-fed ETH (`selfdestruct`/`sendall`)?
  (solodit-hexens-2023-04-14-lido-0-3)
- Do forwarders/relayers let the caller choose the forwarded gas without a
  minimum, allowing a low-gas front-run to consume the victim's nonce?
  (solodit-zokyo-2024-02-26-tide-0-1)
- Do token-standard callbacks (`onERC1155Received`, ERC777) forward
  unbounded gas to recipients, especially inside loops, now that EIP-7702
  EOAs can carry code? (solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0)
- For sequencer/builder-facing flows, can inter-transaction state
  dependencies be crafted to deny multi-round simulation/block building?
  (arxiv-2604.21169)

## Prior incidents

- **GovernMental (2016) — ~1100 ETH stuck**: the jackpot payout looped over
  an ever-growing creditors array until the clearing transaction exceeded
  the block gas limit, freezing the payout — the canonical unbounded-loop
  DoS [cites: swc-128].
- **Tren Finance (audit 2024-11) — High**: `massUpdateRewards`/`removeIdFromList`
  unbounded loops over pool investment IDs could reach the block gas limit
  and block reward updates (resolved by removing the functions)
  [cites: solodit-zokyo-2024-11-19-tren-0-0].
- **Uniswap-v3 limit-order registry (Cyfrin 2023-06) — Medium**: gas-griefing
  DoS on `performUpkeep` by spamming opposite-direction orders so the list
  walk exceeds the upkeep gas budget; fixed by splitting the order book
  [cites: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5].
- **Unicrow (AuditOne 2022-12) — High**: push-payment escrow let any party
  reject funds (reverting contract / ERC777) to block settlement; fixed with
  pull-over-push [cites: solodit-auditone-2022-12-14-unicrow-0-3].
- **Casimir (Cyfrin 2024-07) — High / Medium**: attacker reverting on
  `receive()` blocked the FIFO unstake queue, and `requestUnstake(0)` spam
  inflated the O(n) queue past the gas limit — freezing all unstakes
  [cites: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0,
  solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2].
- **DeXe Governance (Cyfrin 2023-11) — Medium**: return-bomb executors let a
  proposal author guarantee one-sided execution (`actionsAgainst` permanently
  DoS'ed) [cites: solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13].
- **Zerem (Pashov 2022-11) — Medium**: relayer-paid ETH transfer copied
  callee return data to memory, enabling a gas-griefing attack; fixed via
  assembly call [cites: solodit-pashov-audit-group-2022-11-01-zerem-1-2].
- **Lido (Hexens 2023-04) — High**: bad actor force-fed ETH (`selfdestruct`)
  into StakingRouter so a strict accounting assertion failed and reverted
  `deposit` [cites: solodit-hexens-2023-04-14-lido-0-3].
- **Tide (Zokyo 2024-02) — High**: forwarder accepted caller-chosen gas with
  no minimum; a low-gas front-run burned the victim's nonce, denying the
  intended forwarded transaction [cites: solodit-zokyo-2024-02-26-tide-0-1].
- **Myriad CLOB (Cyfrin 2026-03) — Medium**: ERC-1155 `safeTransferFrom`
  callbacks forwarded ~97% of remaining gas to EIP-7702 EOAs inside a match
  loop, letting an index-0 attacker starve settlement
  [cites: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0].

## References

- corpus entries:
  - swc-128 — SWC-128: DoS With Block Gas Limit (canonical pattern + GovernMental)
  - solodit-zokyo-2024-11-19-tren-0-0 — Denial of Service via Unbounded Loops
  - solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5 — Gas griefing DoS on `performUpkeep`
  - solodit-auditone-2022-12-14-unicrow-0-3 — Any party can reject receiving funds (push-payment DoS)
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-0-0 — DoS during unstaking by reverting on ETH receipt
  - solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-1-2 — Spamming `requestUnstake()` to DoS the unstake queue
  - solodit-pashov-audit-group-2022-11-01-zerem-1-2 — Gas griefing/theft on unsafe external call
  - solodit-cyfrin-2023-11-10-cyfrin-dexe-1-13 — Proposal execution DoSed with return bombs
  - solodit-cyfrin-2024-01-10-cyfrin-thermae-2-0 — Use low-level `call()` to prevent gas griefing
  - solodit-zokyo-2023-08-11-velocore-0-1 — Transfer design prone to DOS (atomic batch settlement)
  - solodit-zokyo-2024-02-26-tide-0-1 — DoS via front-run gas-limit manipulation (forwarder/nonce)
  - solodit-guardian-audits-2022-10-24-gmx-1-1 — Potential Gas DoS (unbounded `setPrices` arrays)
  - solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2 — Automation DoS via blacklisted/reverting fee recipients
  - solodit-hexens-2023-04-14-lido-0-3 — Bad actor can block Lido deposit (force-fed ETH + strict check)
  - solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-1-0 — ERC-1155 callbacks forward unbounded gas to EIP-7702 EOAs
  - arxiv-2604.21169 — Position Paper: Denial-of-Service against Multi-Round Transaction Simulation
