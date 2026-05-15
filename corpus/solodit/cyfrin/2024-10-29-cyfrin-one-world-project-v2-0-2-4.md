---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`NativeMetaTransaction::executeMetaTransaction` is unnecessarily `payable`'
vuln_class: []
---

# `NativeMetaTransaction::executeMetaTransaction` is unnecessarily `payable`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `NativeMetaTransaction::executeMetaTransaction` is marked [`payable`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/NativeMetaTransaction.sol#L33-L39) but, unlike the [OpenZeppelin implementation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/49c0e4370d0cc50ea6090709e3835a3091e33ee2/contracts/metatx/MinimalForwarder.sol#L55), the [`low-level call`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/NativeMetaTransaction.sol#L62-L64) in the function body does not forward any native token. Hence, any native token balance sent as part of the transaction will be stuck in the implementing contract.

**Impact:** In the case of `MembershipFactory`, native token balances can be rescued by the `EXTERNAL_CALLER` role, but for `OWPIdentity` any native token would be stuck forever.

**Recommended Mitigation:** Consider removing `payable` from `NativeMetaTransaction::executeMetaTransaction`, since native token is not used in any of the contracts and so it is not needed.

There is also [a comment](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/NativeMetaTransaction.sol#L22-L23) about the `MetaTransactionStruct` that could then be reworded to say  _"value isn't included because it is not used in the implementing contracts"_.

**One World Project:** Updated in [`e60b078`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/e60b078f09d4ed0f1e509f36a2a6d42293815737)

**Cyfrin:** Verified. `msg.value` is now forwarded.

\clearpage
