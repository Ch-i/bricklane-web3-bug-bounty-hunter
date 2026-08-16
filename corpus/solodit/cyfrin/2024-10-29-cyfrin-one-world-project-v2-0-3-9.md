---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Incorrect `EIP712Base` constructor documentation
vuln_class: []
---

# Incorrect `EIP712Base` constructor documentation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** [This comment](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/EIP712Base.sol#L21-L29) documenting the `EIP712` constructor is incorrect:

```solidity
// supposed to be called once while initializing.
// one of the contractsa that inherits this contract follows proxy pattern
// so it is not possible to do this in a constructor
```

The only contract in the project using a proxy pattern is `MembershipERC1155` which does not inherit `EIP712Base` directly or otherwise. Hence, the comment is not needed.

There is also a typo:

```diff
-  // one of the contractsa that inherits this contract follows proxy pattern
+  // one of the contracts that inherits this contract follows proxy pattern
```

**One World Project:** Removed in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. The documentation is now removed.
