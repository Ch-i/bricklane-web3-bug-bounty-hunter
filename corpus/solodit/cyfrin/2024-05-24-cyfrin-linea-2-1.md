---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-2-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Linea can bypass validity proof verification for L2->L1 block finalization
vuln_class: []
---

# Linea can bypass validity proof verification for L2->L1 block finalization

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** One major advantage of using zk rollups over Optimistic rollups is that zk rollups use math & cryptography to verify L2->L1 block finalization via a validity proof which must be submitted and verified.

In the current codebase the Linea team has two options to bypass validity proof verification during block finalization:

1) Explicitly by calling `LineaRollup::finalizeBlocksWithoutProof` which takes no proof parameter as input and doesn't call the `_verifyProof` function.

2) More subtly by calling `LineaRollup::setVerifierAddress` to associate a `_proofType` with a `_newVerifierAddress` that implements the `IPlonkVerifier::Verify` interface, but which simply returns `true` and doesn't perform any actual verification. Then call `LineaRollup::finalizeBlocksWithProof` passing `_proofType` associated with `_newVerifierAddress` which will always return true.

**Impact:** Using either option makes Linea roughly equivalent to an Optimistic roll-up but without Watchers and the ability to challenge. That said if either option is used, `LineaRollup::_finalizeBlocks` always executes which enforces many "sanity checks" that significantly limit how these options can be abused.

The "without proof" functionality can also be used to add false L2 merkle roots which could then be used to call `L1MessageService::claimMessageWithProof` to drain ETH from the L1.

**Recommended Mitigation:** Linea is still at the alpha stage so these functions are likely needed as a last resort. Ideally once Linea is more mature such functionality would be removed.

**Linea:**
Acknowledged; the ability to finalize blocks without proof is primarily part of our "training wheels" controlled via the Security Council, analyzed by Security partners and reserved for particular cases like we had when we upgraded our state manager to another hashing algorithm (the last time it was used).
