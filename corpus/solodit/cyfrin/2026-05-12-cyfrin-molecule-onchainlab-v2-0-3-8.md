---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLabFactory::initializeAccount` doesn''t check the existence of the
  token'
vuln_class: []
---

# `OnChainLabFactory::initializeAccount` doesn't check the existence of the token

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Anyone can pre-deploy an off-canonical 6551 account (via direct `ERC6551Registry::createAccount` with arbitrary salt) and then call `factory.initializeAccount(thatAccount)` to install canonical attesters/registry on it. Future protocol upgrades that change canonical attesters/threshold leave any pre-initialized account locked to the OLD config (factory's idempotent `try/catch AlreadyInitialized` swallows the error). Off-chain indexers see initializations for non-canonical accounts polluting `RegistryConfigured` events.

The issue is not just the availability to initialize any wallet, but since `ERC6551Registry` is publicly accessible, the Users can compute TBA accounts for tokens that are not minted at `LabNFT`, allowing them to:

- Create TBA account for a token that does not exist.
- Initialize it too.

**Files:**

`src/factory/OnChainLabFactory.sol:200-203`.

**Recommended Mitigation:** We should check that the tokenOwner to be initialized is not `address(0)` so that we are sure that the token is created and exists, and we are not initializing an account of a ghost token.

We can't prevent TBA creation of ghost tokens, as it is handled by `ERC6551Registry::createAccount`, but they should not get initialized before the token is created.

**Molecule:** Fixed in [1c054ad](https://github.com/moleculeprotocol/onchainlabs/commit/1c054ad).

**Cyfrin:** Verified.
