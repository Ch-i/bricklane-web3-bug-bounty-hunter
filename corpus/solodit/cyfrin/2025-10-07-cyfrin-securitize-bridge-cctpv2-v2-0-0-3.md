---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Bridging `DSToken` back-and-forth between chains causes `totalIssuance` cap
  to be reached, preventing further issuances and cross-chain transfers
vuln_class: []
---

# Bridging `DSToken` back-and-forth between chains causes `totalIssuance` cap to be reached, preventing further issuances and cross-chain transfers

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** `StandardToken::totalIssuance` is not decreased by burns but is used to enforce maximum cap, since `totalIssuance` is supposed to track the total number of tokens ever issued, not the current "supply".

However there is an interesting consequence to this when considering cross-chain bridging via `SecuritizeBridge`; `receiveWormholeMessages` calls `DSToken::issueTokens` on the destination chain which increases `StandardToken::totalIssuance`.

**Impact:** Consider this scenario:
* Alice bridges from Ethereum -> Arbitrum with 1000 `DSToken`
* Alice bridges back from Arbitrum -> Ethereum with the "same" 1000 `DSToken`
* Alice keeps doing this over and over again

This process continually increases the `totalIssuance` on both chains, even though it is just the same tokens going back and forth; at some point this will cause the cap to be hit on one of the chains. This doesn't even require malicious investors, just investors who bridge back-and-forth frequently.

Once the cap is hit further issuances and cross-chain transfers will revert on that chain.

**Recommended Mitigation:** Potential mitigations include:
* have bridging actually decrement `totalIssuance` on the source chain
* have `SecuritizeBridge::receiveWormholeMessages` call `DSToken::issueTokensCustom` passing a `reason == "BRIDGING"` then  in `TokenLibrary::issueTokensCustom` don't increment `totalIssuance` for `"BRIDGING"` reason
* track the number of bridged tokens separately and modify the cap check to account for this

**Securitize:** Fixed in commit [c2e62c9](https://github.com/securitize-io/dstoken/commit/c2e62c9c1137bb7c6f548b72f960d864c42445fc); the cap was deprecated and associated checks removed. There is a similar compliance-related check that uses `totalSupply` so correctly accounts for burns.

**Cyfrin:** Verified.

\clearpage
