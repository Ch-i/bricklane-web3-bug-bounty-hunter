---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Unchained initializers should be called in `PausableOwnable::__PausedOwnable_init`
  instead
vuln_class: []
---

# Unchained initializers should be called in `PausableOwnable::__PausedOwnable_init` instead

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

While not an immediate issue in the current implementation, the direct use of initializer functions rather than their unchained equivalents should be avoided. These have been implemented and used in some places but not others, for example, [`__PausedOwnable_init`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/libraries/PausableOwnable.sol#L26-L29) which should be modified to avoid [potential duplicate initialization](https://docs.openzeppelin.com/contracts/5.x/upgradeable#multiple-inheritance) in future.

```solidity
function __PausedOwnable_init(address initialPauser, address owner) internal onlyInitializing {
    __Paused_init(initialPauser);
    __Ownable_init(owner);
}
```

**Wormhole Foundation:** This has been reviewed and has to impact on the current contracts. Any contract changes in the future will be reviewed, including changes to libraries.

**Cyfrin:** Acknowledged.
