---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[I-04] Lack of two step ownership transfers'
vuln_class: []
---

# [I-04] Lack of two step ownership transfers

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Original severity:** Best Practices

**Files:** [`transfer_ownership.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/transfer_ownership.rs), [`transfer_program_admin.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/transfer_program_admin.rs)

**Description:**

The program provides instructions for transferring ownership of the program admin and for the individual unlocker accounts (Projects). Those instructions allow transfer of the ownership to any arbitrary account. Currently, best practice dictates that there should be some form of control over who the ownership is transferred to. This, in a classical Solidity implementation, would involve two separate calls. On Solana, this can be done in a simplified way - there would still be a single instruction however there should be a requirement added to the instructions’ contexts that the new address should also be a Signer.

**Impact:** Accidental loss of control over the protocol or unlocker accounts.

**Recommendation:** Ensure Signer type of account for new owner accounts.

**Status:** Acknowledged

**Update from TokenTable:** Changed to two-step ownership transfers (using two transaction signers) in [4a176e0a](https://github.com/EthSign/tokentable-unlocker-solana/tree/4a176e0a4cfbaf9fa5aaa20b8b57e122e72d7cb3). This logic was amended in [89889a1fef4fe1f879818eb8e2b8a6d80e8b76de](https://github.com/EthSign/tokentable-unlocker-solana/tree/89889a1fef4fe1f879818eb8e2b8a6d80e8b76de), allowing the second signer to be null in calls to `transfer_ownership()` and `transfer_program_admin()`. In this case, the new owner/admin must call `receive_ownership()` or `receive_program_admin()`, respectively, to complete the permission transfer. After additional internal discussion, we have elected to roll back the two-step ownership transfer modifications for `transfer_ownership()` in [3dbd4b333432893f482acc7dc12b947c54ce324f](https://github.com/EthSign/tokentable-unlocker-solana/tree/3dbd4b333432893f482acc7dc12b947c54ce324f). The added complexity does not justify the risks in typical usage (limited frontend verification is performed).
