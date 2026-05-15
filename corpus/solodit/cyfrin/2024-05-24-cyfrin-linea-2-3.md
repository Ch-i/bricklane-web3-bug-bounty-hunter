---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Potential L1->L2 `ERC20` decimal inconsistency can result in loss of user bridged
  tokens
vuln_class: []
---

# Potential L1->L2 `ERC20` decimal inconsistency can result in loss of user bridged tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** The first time a new ERC20 token is bridged, `TokenBridge::bridgeToken` uses the `IERC20MetadataUpgradeable` interface to fetch the token's name, symbol and decimals in order to create a bridged version of the token.

If the `staticcall` to `IERC20MetadataUpgradeable::decimals` fails to return a valid value then `TokenBridge::_safeDecimals` defaults to 18 decimals.

**Impact:** This is potentially dangerous as:
* a non-standard ERC20 token could be using a non-18 decimal value internally but not have a `decimals` function
* the newly created bridged version will have 18 decimals different to the native token

When the user attempts to bridge back, the user's bridged tokens will be burned and then on the native chain:
* if the native token has less than 18 decimals, the transfer call will revert resulting in the user's originally bridged tokens stuck in the token bridge
* if the native token has greater than 18 decimals, the transfer call will succeed resulting in the user receiving less tokens than they initially bridged over

**Recommended Mitigation:** `TokenBridge::_safeDecimals` should revert if the token being bridged does not return its decimals from the call to `IERC20MetadataUpgradeable::decimals`. Interestingly Consensys itself reported the same finding as issue 5.4 in their [Nov 2021 Arbitrum audit](https://github.com/OffchainLabs/nitro/blob/master/audits/ConsenSys_Diligence_Arbitrum_Contracts_11_2021.pdf).

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L435-R446) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L435-R449).

**Cyfrin:** Verified.

\clearpage
