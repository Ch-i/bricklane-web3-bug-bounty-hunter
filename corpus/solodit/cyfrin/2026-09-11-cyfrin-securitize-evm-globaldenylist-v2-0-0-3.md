---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0-0-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-11T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-11-cyfrin-securitize-evm-globaldenylist-v2-0
title: Sanctioned addresses can be registered as investor or special wallets in breach
  of OFAC FAQ42
vuln_class: []
---

# Sanctioned addresses can be registered as investor or special wallets in breach of OFAC FAQ42

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-11-cyfrin-securitize-evm-globaldenylist-v2.0.md)_

---

**Description:** A wallet address enters the protocol through one of two independent registries, and neither consults the global denylist at any point. A globally denylisted address can therefore be registered as an investor wallet or assigned a special wallet type after it has been designated.

Investor wallets are held by `RegistryService`. All three entry points are `onlyExchangeOrAbove`, except `WalletRegistrar::registerWallet` which is `onlyOwnerOrIssuerOrAbove`:

1. `RegistryService::addWallet` - binds one address to an existing investor, and is the single internal choke point every investor wallet passes through
2. `RegistryService::updateInvestor` - iterates its `_wallets` argument and calls `addWallet` for each address not already registered
3. `WalletRegistrar::registerWallet` - delegates directly to `updateInvestor`

Special wallets are held by `WalletManager`. All five entry points are `onlyIssuerOrAbove` and all funnel into the internal `WalletManager::setSpecialWallet`:

4. `WalletManager::addIssuerWallet` - assigns type `ISSUER`
5. `WalletManager::addIssuerWallets` - bulk form, capped at 30 addresses
6. `WalletManager::addPlatformWallet` - assigns type `PLATFORM`
7. `WalletManager::addPlatformWallets` - bulk form, capped at 30 addresses
8. `WalletManager::addExchangeWallet` - assigns type `EXCHANGE`, and additionally requires the supplied owner to hold the exchange role

Both choke points already perform registration-time validation, so the pattern of rejecting an ineligible address at the point of registration is established. `RegistryService::addWallet` rejects an address that already carries a special wallet type and rejects one holding a non-zero balance. `WalletManager::setSpecialWallet` rejects an address that already belongs to an investor and rejects a direct type change. The global denylist is simply absent from both sets of checks.

The global denylist is intended to be a protocol-wide ban expressing sanctions designations. [OFAC FAQ 42](https://ofac.treasury.gov/faqs/42) addresses this situation directly and treats onboarding, rather than transacting, as the prohibited act:

> What do I do if a person tries to open an account and the individual or entity's name is on OFAC's SDN List (or is otherwise a blocked person)? Do I open the account and then block the funds?
>
> A U.S. financial institution, its foreign branches, and - in some cases - its wholly-owned or -controlled foreign subsidiaries, cannot open an account for a person named on OFAC's List of Specially Designated Nationals and Blocked Persons (SDN List) or a person who is otherwise blocked (e.g., a blocked government or an entity that is subject to the 50 Percent Rule). This is a prohibited service.

[OFAC FAQ 560](https://ofac.treasury.gov/faqs/560) confirms the obligation is identical on-chain:

> Are my OFAC compliance obligations the same, regardless of whether a transaction is denominated in digital currency or traditional fiat currency?
>
> Yes, the obligations are the same.

[OFAC FAQ 1021](https://ofac.treasury.gov/faqs/1021) extends it explicitly to wallet-level service providers:

> U.S. persons, including virtual currency exchanges, virtual wallet hosts, and other service providers ... are generally prohibited from engaging in or facilitating prohibited transactions, including virtual currency transactions in which blocked persons have an interest.

Registering a wallet address is the on-chain analogue of opening an account: it is the step that binds an address to an identity or a role inside the platform and makes it eligible to hold and move a token. The point of FAQ 42 is that the prohibition attaches at that moment, not only when value later moves. A control that screens transfers but not registration therefore permits the one step FAQ 42 names as prohibited in its own right, and today the only signal that anything is wrong appears later, when a transfer or issuance involving that wallet is rejected.

**Recommended Mitigation:** Before registering any new address in the protocol, consult the global deny list and revert if that address is sanctioned.

**Securitize:** Acknowledged; on investor wallets (`RegistryService::addWallet`) PERMISSIONLESS-compliance token (the only compliance type with a working global denylist) deploys with `StubRegistryService` by default , whose `addWallet` is a pure no-op. Since `ComplianceServicePermissionless` never consults investor-registry data for authorization in the first place (only the denylist/blacklist checks gate transfers), the fix as suggested would be dead code on the one compliance path where it could matter.

On special wallets (`WalletManager::setSpecialWallet`, issuer/platform/exchange) assigning any of these roles is already gated by `onlyIssuerOrAbove` a privileged, internal action taken by the issuer/platform operator, not a customer-facing self-service flow like investor onboarding. Platform/issuer/exchange wallets are Securitize/issuer-controlled operational infrastructure, not third-party accounts, so the entity granting the role already knows who it's assigning it to.

\clearpage
