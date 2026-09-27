---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2-0
title: '`setup-governance` surrenders `ROLE_MASTER` before confirming every ownership
  transfer succeeded, so a silently skipped owner mismatch leaves a live `ROLE_ISSUER`
  proxy outside the timelock and is detected only after the step is irreversibl'
vuln_class: []
---

# `setup-governance` surrenders `ROLE_MASTER` before confirming every ownership transfer succeeded, so a silently skipped owner mismatch leaves a live `ROLE_ISSUER` proxy outside the timelock and is detected only after the step is irreversible

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-07-cyfrin-securitize-evm-dstoken-timelocks-v2.0.md)_

---

**Description:** `setup-governance` invoked with `--handover` builds a list of `Ownable` services from `OWNED_SERVICE_IDS` plus the token, then walks it transferring each `owner` to the master timelock. Where the current owner is not the signer, the task cannot transfer it, because `transferOwnership` is owner-gated. It prints a line and moves to the next entry:

```typescript
const currentOwner = await ownable.owner();
if (currentOwner.toLowerCase() !== signer.address.toLowerCase()) {
  console.log(`  ${name} (${address}): owner is ${currentOwner}, skipping`);
  continue;
}
```

A non-`Ownable` target is swallowed by the surrounding `catch` in the same way. Neither outcome sets a failure flag, and the loop has no post-condition. Immediately after it, the task calls `TrustService::setServiceOwner` to move `ROLE_MASTER` to the master timelock, which its own log line describes as the final step and irreversible for the signer. Only after that does it invoke `verify-governance` with `handedOver` set, which does compare each service `owner` against the master timelock and throws on mismatch.

The ordering is the defect. A skipped transfer is real and is reported, but only once authority has already been surrendered, and the signer no longer has the standing to correct it. There is no pre-flight pass that resolves every expected owner and refuses to proceed while any of them is not the signer.

This is reachable on current mainnet state rather than hypothetical. On ACRED at block 25845400, service id 1024 resolves to a `WalletRegistrar` proxy whose `owner` is `0x3EE611d581d2C6A81459FfF8C6c8d197B0aD1A3E`, an externally owned account that holds no role in `TrustService` and owns no other service in the deployment. The token's `ROLE_MASTER` holder and the owner of every other listed service is a different address, `0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee`. That `WalletRegistrar` proxy itself holds `ROLE_ISSUER` on the live token. Running the documented handover against this deployment therefore takes the skip branch for one entry, surrenders `ROLE_MASTER`, and only then fails verification.

**Spec-Intent Gap:**

`timelocks.pdf` FR-4 states:

> Handover transfers every service owner() and the trust service master role to the master timelock, after which upgrade authorization and service pointer changes require its queue.

The task's own documentation makes the same commitment, stating that with `--handover` it transfers every owner to the master timelock and finally `TrustService` master itself, after which the signer has no authority left. The implementation transfers only those owners that happen to already be the signer, and surrenders master authority whether or not the rest succeeded.

**Impact:** An operator following the documented sequence ends in a state the tooling describes as complete handover but which is a partial one. `ROLE_MASTER` has moved irreversibly, while at least one proxy holding `ROLE_ISSUER` on a live token remains under an unrelated externally owned account that retains instant upgrade authority over it. Because upgrading a proxy does not change its address, that key can replace the implementation and exercise the proxy's existing issuance identity against the token without passing through any timelock.

The same branch applies to any listed service whose owner has drifted from the signer for any reason, so the exposure is not specific to one contract.

**Proof of Concept:**
1. Resolve the owner of service id 1024 on ACRED and confirm it differs from the token's `ROLE_MASTER` holder, and that the proxy holds `ROLE_ISSUER`:

```shell
# ACRED on Ethereum mainnet, pinned to a block so the values below are reproducible
export ETH_RPC_URL=<ethereum mainnet rpc>
BLOCK=25845400
ACRED=0x17418038ecf73ba4026c4f428547bf099706f27b

# every other address is derived, nothing needs to be looked up by hand
TRUST=$(cast call --block $BLOCK $ACRED "getDSService(uint256)(address)" 1)
# 0xc397436742eAF7C325DDBFc4dc63D95822b27101
WALLET_REGISTRAR=$(cast call --block $BLOCK $ACRED "getDSService(uint256)(address)" 1024)
# 0xDdf17A432B312a6C0E42F3B34ADBE914B12cb44F
WR_OWNER=$(cast call --block $BLOCK $WALLET_REGISTRAR "owner()(address)")
# 0x3EE611d581d2C6A81459FfF8C6c8d197B0aD1A3E

# the owner of service id 1024 is not the address that holds ROLE_MASTER
cast call --block $BLOCK $ACRED "owner()(address)"
# 0x59c1eAcEc450c57Dcb9b8725d0F96635C2b676Ee

# yet that proxy holds ROLE_ISSUER, while its owner holds no role at all
cast call --block $BLOCK $TRUST "getRole(address)(uint8)" $WALLET_REGISTRAR
# 2, ROLE_ISSUER
cast call --block $BLOCK $TRUST "getRole(address)(uint8)" $WR_OWNER
# 0, no role
```

2. Run `setup-governance --handover` as the signer holding `ROLE_MASTER`; the loop reaches id 1024, finds an owner that is not the signer, prints its skip line and continues
3. The task proceeds to `setServiceOwner`, moving `ROLE_MASTER` to the master timelock; the signer now has no authority
4. The task then runs `verify-governance` with `handedOver` set, which fails the owner assertion for that entry. The operator learns of the incomplete handover after the irreversible step, and cannot remedy it, since the residual owner is a key they do not control

**Recommended Mitigation:** Separate discovery from mutation, and make the irreversible step conditional on the rest having succeeded.

1. Add a pre-flight pass that resolves the expected owner of every target before any transaction is sent, and aborts with the complete list of mismatches when any expected owner is not the signer, so the operator resolves them while still holding authority
2. Treat both the owner mismatch and the non-`Ownable` catch as failures rather than log-and-continue, and collect them instead of returning at the first one
3. Send `setServiceOwner` only after every ownership transfer has been confirmed on-chain, and run the verification checklist before the irreversible step as well as after it, so a failed assertion prevents handover rather than merely recording that it was incomplete

**Securitize:** Fixed in commits [eadeeab](https://github.com/securitize-io/dstoken/commit/eadeeab517275b746abc65e46f46649a1728da8b), [99283d6](https://github.com/securitize-io/dstoken/commit/99283d65d240eac2fc3c87d6bcf4a2baefd82fde) by:
* defining all service IDs including deprecated/legacy in new file `tasks/utils/governed-services.ts`
* improved pre-flight and verification scripts to check/verify every transferable contract and abort before moving ownership if a contract is not owned by the signer
* runs the full verifier with `ownersHandedOver: true` while the signer still holds `ROLE_MASTER`
* verification asserts both ownership and that each service resolves the expected `TrustService`
* calls `setServiceOwner` only after all those checks pass

**Cyfrin:** Verified.
