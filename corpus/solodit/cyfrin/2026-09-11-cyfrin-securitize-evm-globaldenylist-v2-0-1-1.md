---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-1-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: '`deploy-all` does not await `GlobalDenyListManager::addOperator, changeAdmin`
  receipts and reports success on unconfirmed transactions'
vuln_class: []
---

# `deploy-all` does not await `GlobalDenyListManager::addOperator, changeAdmin` receipts and reports success on unconfirmed transactions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** `deploy-all` sends the two role handover transactions as `await globalDenylistManager.addOperator(...)` and `await globalDenylistManager.changeAdmin(...)`. In ethers v6 that promise resolves to a `ContractTransactionResponse` once the node accepts the transaction into the mempool, not once it is mined; the resolved object exposes `wait` and carries no `status`. Neither call invokes `wait`, so the task returns and the process exits with both transactions still unconfirmed.

**Impact:** The task prints its handover lines and exits zero regardless of the on-chain outcome; the role transfer transactions may never end up successfully executing but the deployer mistakenly believes they have because of the print output.

This outcome conflicts with the following section in `GlobalDenylist-AuditScope.md` which states:

> `S-1 — Admin handover silently fails, leaving the deployer as permanent root admin`
>
> `deploy-all` calls `changeAdmin` and returns without asserting the outcome. If the target already held `DEFAULT_ADMIN_ROLE` (granted out of band through the permissive `grantRole` override), Operations believes the ephemeral deployer key was decommissioned while it retains upgrade, pause, and role-granting authority over a platform-wide contract. A short-circuit variant of this was found and fixed during development; verify no residual path reproduces it.

**Recommended Mitigation:** Await the receipt for each role transaction, keeping both calls inside their existing zero-address guards:

```typescript
if (args.operator !== ZeroAddress) {
  await (await globalDenylistManager.addOperator(args.operator)).wait();
}
if (args.admin !== ZeroAddress) {
  await (await globalDenylistManager.changeAdmin(args.admin)).wait();
}
```

`wait` resolves only after the transaction is mined and throws `CALL_EXCEPTION` when the receipt carries a `status` of zero, which is exactly the revert case pre-flight gas estimation cannot catch. It also throws when the transaction was replaced at the same nonce. Bound the call as `wait(1, timeoutMs)` so a stuck transaction cannot block indefinitely, since the default timeout is zero, and raise the confirmation count above the default of one on chains where reorg depth matters.

**Securitize:** Fixed in commit [4f7632d](https://github.com/securitize-io/bc-global-denylist-manager-sc/commit/4f7632df14bd94fd5ded7a6c50a3481394b4af21).

**Cyfrin:** Verified.
