---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-14
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` can never execute mint step'
vuln_class: []
---

# `deploy-full.ts` can never execute mint step

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** `deploy-full.ts` signs every transaction with the deployer, so its mint branch is conditioned on the configured issuer being the deployer:

```typescript
if (issuerWallet.toLowerCase() === deployer.address.toLowerCase()) {
  await retry(async () => {
    await (await tok.mint(INVESTOR_WALLET, ethers.parseUnits(MINT_AMOUNT, dec))).wait();
  }, 'mint');
}
```

However, the configuration validation immediately before `deployTrustStack` rejects that exact relationship:

```typescript
if (
  issuerWallet.toLowerCase() === deployer.address.toLowerCase() ||
  transferAgentWallet.toLowerCase() === deployer.address.toLowerCase()
) {
  throw new Error('ISSUER_WALLET / TRANSFER_AGENT_WALLET must not be the deployer (it holds MASTER).');
}
```

Consequently, every configuration that reaches the mint condition necessarily makes it false. A configuration that would make it true is rejected earlier.

**Impact:** Dead code and a mismatch between the script's full-deployment behavior and its executable behavior.

**Recommended Mitigation:** Consider removing the unreachable mint branch and `MINT_AMOUNT` configuration from `deploy-full.ts` and document the required post deployment issuer transaction.

**Securitize:** Fixed in [PR 17](https://github.com/securitize-io/bc-tempo-sc/pull/17).

**Cyfrin:** Verified.
