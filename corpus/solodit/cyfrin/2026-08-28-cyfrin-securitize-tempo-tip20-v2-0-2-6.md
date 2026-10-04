---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-28-cyfrin-securitize-tempo-tip20-v2-0-2-6
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-28-cyfrin-securitize-tempo-tip20-v2-0
title: '`deploy-full.ts` permits overlapping operational role addresses'
vuln_class: []
---

# `deploy-full.ts` permits overlapping operational role addresses

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-28-cyfrin-securitize-tempo-tip20-v2.0.md)_

---

**Description:** The script takes three addresses from the environment — issuer, transfer agent and token owner — and checks only that the issuer and transfer agent aren't the deployer (`:328-333`). Nothing compares them to each other, and nothing checks the token owner at all.

Four overlaps are possible, and they don't behave the same way.

**Issuer and transfer agent set to the same address.** Abstract roles are exclusive, so `setRole(x, ISSUER)` followed by `setRole(x, TRANSFER_AGENT)` (`:216-221`) replaces the first rather than adding to it. That account is left without the issuer role, so it can't mint, onboard investors or lock them — only the token owner can, through `MASTER`. So you lose the separate issuer you configured, not the capability. The script still prints success. It's recoverable: the token owner grants `ISSUER` back in one transaction.

**Issuer or transfer agent set to the token owner's address.** Harmless. `setServiceOwner` runs last (`:241`) and promotes that account to `MASTER`, whose native grants cover everything `ISSUER` and `TRANSFER_AGENT` project. The operator ends up with more authority, not less.

**Token owner set to the deployer's address.** Here the effect is permanent. The handover grants `DEFAULT_ADMIN_ROLE` to the token owner on the token, registry and ServiceConsumer (`:244-246`), then has the deployer renounce its own on the same three (`:248-250`). Same address, so the grant does nothing — the account already holds the role — and the renounce then removes it. All three end up with nobody holding admin.

That role administers itself, so once there are no holders it can never be granted again, and the registry's upgrade function is gated on it (`Tip20RegistryService.sol:132`). The deployer keeps `MASTER` on the trust, so lock and unlock still work, but the script renounces `REGISTRAR_ROLE` one line after the handoff re-granted it, so registering new investors reverts from the moment the deploy ends. That part is repairable by handing `MASTER` through a second key and back. The lost `DEFAULT_ADMIN_ROLE` is not. Confirmed by running it.

The script already carries a comment at `:313-319` explaining why `TOKEN_OWNER` must not default to the deployer, so this class of mistake was considered — the checks just don't cover it.

**Recommended Mitigation:** Extend the check at `:328-333` so it rejects two configurations before any transaction is sent: the token owner equal to the deployer, and the issuer equal to the transfer agent unless that address is also the token owner. Anything the token owner shares an address with is safe, because it ends up as `MASTER` either way.

**Securitize:** Fixed in [PR 17](https://github.com/securitize-io/bc-tempo-sc/pull/17).

**Cyfrin:** Verified.
