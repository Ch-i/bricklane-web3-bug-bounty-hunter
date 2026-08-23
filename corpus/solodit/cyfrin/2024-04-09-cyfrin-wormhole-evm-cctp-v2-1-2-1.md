---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Potential accounting error when the decimals of bridged assets differ between
  CCTP domains
vuln_class: []
---

# Potential accounting error when the decimals of bridged assets differ between CCTP domains

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

The `FiatTokenV2_2` contract deployed to target CCTP domains typically has 6 decimals; however, on some chains, such as BNB Smart Chain, a decimal value of 18 is used. The Wormhole CCTP integration contract and the core CCTP contracts themselves do not reconcile any differences in the source/destination token decimals, which would cause critical issues in the amount to be minted on the target domain since these contracts are not working with Wormhole x-assets (where this issue is sufficiently mitigated) but rather native USDC/EURC on the respective chains.

For example, assuming both CCTP domains are intended to be supported, burning 20 tokens on BNB Smart Chain where USDC has 18 decimals, encoded as `20e18`, then trying to mint this amount on the destination chain where USDC has 6 decimals (e.g. Ethereum), then there is a problem because the recipient has not, in fact, minted `20e12` tokens instead of 20.

Since BNB Smart Chain is not one of the currently supported domains, and all currently supported CCTP domains use a version of the `FiatTokenV2_2` contract with 6 decimals, this is not an issue at present. If a non-standard domain is ever intended to be supported for cross-chain transfers, then it is important that any differences in the token decimals are correctly reconciled.

**Wormhole Foundation:** No need to change anything now but will have to make changes if CCTP introduces other chains. One to be aware of and keep and eye on going forwards.

**Cyfrin:** Acknowledged.
