---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-06-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2-0
title: '`getWhitelistIxs` is not checking the ownership of the tokenAccounts passed
  with tx owner'
vuln_class: []
---

# `getWhitelistIxs` is not checking the ownership of the tokenAccounts passed with tx owner

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-02-cyfrin-securitize-svm-whitelist-acl-support-v2.0.md)_

---

**Description:** When constructing a whitelist transaction, the off-chain `getWhitelistIxs` function is called. The caller can either provide token accounts directly via `params.tokenAccounts`, or omit them — in which case the function automatically derives the owner's Associated Token Accounts (ATAs).

The problem arises when token accounts are provided explicitly. In this case, there is no off-chain validation to verify that the provided token accounts are actually owned by the transaction owner, allowing arbitrary token accounts to be passed without any client-side rejection.

> packages/spl-token-whitelist-sdk/src/instructions/whitelist.ts#getWhitelistIxs
```ts
export async function getWhitelistIxs( ... ): Promise<TransactionInstruction[]> {
  ...
  let tokenAccounts: PublicKey[];

  if (params.tokenAccounts && params.tokenAccounts.length > 0) {
>>  tokenAccounts = params.tokenAccounts;
  } else { ... }

  ...

  return [...preIxs, ix];
}
```

While the on-chain program does enforce that each token account's owner matches the transaction signer, the absence of this check on the client side means that a caller can construct and submit a transaction referencing token accounts they do not own. The transaction will be rejected on-chain, but the SDK silently allows the construction and submission of such invalid transactions without providing any meaningful client-side error, leading to a poor developer experience and potentially unexpected runtime failures.

> programs/spl-token-whitelist/src/instructions/whitelist.rs#whitelist_handler
```rs
pub fn whitelist_handler<'info>(ctx: Context<'_, '_, '_, 'info, Whitelist<'info>>) -> Result<()> {
    ...
    // Thaw the token accounts
    for token_account_info in token_accounts_infos.iter() {
        ...
        require!(
>>          token_account.owner == ctx.accounts.owner.key(),
            SplWhitelistErrorCode::InvalidOwner
        );
        ...
    }
    ...
}
```

**Recommended Mitigation:** The `getWhitelistIxs` function should validate that each explicitly provided token account is owned by the transaction owner before constructing the instruction. This check should be performed by fetching each token account's data and verifying that its `owner` field matches the provided owner address.

**Securitize:** Fixed in [db2c3c2](https://github.com/securitize-io/bc-solana-whitelist-sc/commit/db2c3c21026b66b0f06c5fdf59d3ab158a62d078).

**Cyfrin:** Verified.
