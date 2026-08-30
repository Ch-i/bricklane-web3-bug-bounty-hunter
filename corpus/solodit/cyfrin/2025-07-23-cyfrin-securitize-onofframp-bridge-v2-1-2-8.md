---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-2-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: Usage of unofficial wormhole-solidity-sdk npm package poses security and maintenance
  risks
vuln_class: []
---

# Usage of unofficial wormhole-solidity-sdk npm package poses security and maintenance risks

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The bridge contracts in the codebase are using `wormhole-solidity-sdk` version 0.9.0 from npm, which has been confirmed by the Wormhole team to be an unofficial deployment. According to the Wormhole team, the npm package published by `sullof <francesco@sullo.co>` is not their official release, and the only approved version is v0.1.0 available on GitHub. The official recommended approach is to use `forge install wormhole-foundation/wormhole-solidity-sdk@v0.1.0`.

The following contracts are affected by this issue:
- `SecuritizeBridge.sol` - imports `IWormholeReceiver` and `IWormholeRelayer`
- `WormholeCCTPUpgradeable.sol` - imports `IWormholeRelayer`, `IWormhole`, and `ITokenMessenger`
- `USDCBridge.sol` - inherits from `WormholeCCTPUpgradeable` via `CCTPSender` and `CCTPReceiver`
- `RelayerMock.sol` - imports `IWormholeRelayer`

The unofficial package is declared as a dependency in `package.json` with `"wormhole-solidity-sdk": "^0.9.0"` and is used throughout the bridge implementation for cross-chain message passing and CCTP (Circle Cross-Chain Transfer Protocol) functionality.

**Impact:** Using an unofficial SDK introduces potential security vulnerabilities, compatibility issues, and maintenance challenges as the codebase depends on unverified third-party code.

**Recommended Mitigation:** Replace the unofficial npm package with the official GitHub release.

**Securitize:** Fixed in commit [1da35c](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/1da35cde31a53e7b2de56de0d313ebdcb80cbfa3).

**Cyfrin:** Verified. We posted a [tweet](https://x.com/hansfriese/status/1945048296461848901) to alert others using the package, and the author replied, confirming it was intended solely for personal use, not for protocols. To prevent further confusion, the author has taken down the [package](https://x.com/sullof/status/1945490920809304324).

\clearpage
