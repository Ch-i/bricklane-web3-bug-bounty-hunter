---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: ERC-7702 Benefactors Are Not Supported by Signature Verification Logic
vuln_class: []
---

# ERC-7702 Benefactors Are Not Supported by Signature Verification Logic

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** The signature verification logic in `USBDMinting` relies on `address.code.length` to distinguish EOAs from contract accounts. If `benefactor.code.length == 0`, `ECDSA` signatures are accepted; otherwise, the contract falls back to ERC-1271 validation unless delegated signers are configured.

With `ERC-7702`, an EOA can have non-empty code (delegation indicator) while still behaving as a transaction-initiating account. In this case, a benefactor using `ERC-7702` without protocol-level delegated signers will be treated as a contract account and forced through `ERC-1271` validation. If the delegated logic does not explicitly implement `ERC-1271` signature validation, otherwise valid `ECDSA` signatures from the benefactor will be rejected.

As a result, ERC-7702-based benefactors are effectively unsupported unless their delegated contract explicitly handles signature validation in a compatible way. This behavior is implicit and not documented.

**Recommended Mitigation:** Avoid relying on address.code.length as an EOA/contract discriminator for signature handling, or explicitly document that ERC-7702 benefactors must implement ERC-1271-compatible signature validation (or use delegated signers) to interact with the protocol.

**Boudary:**
Resolved. We align with OpenZeppelin's stance on this matter (see [Issue 5707](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/5707)). When a user delegates their EOA via ERC-7702, they explicitly opt into that contract's behavior. Bypassing their delegation choice to force ECDSA verification would override their intent. Documentation clarified in [PR#178](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/178).

**Cyfrin:** Verified.
