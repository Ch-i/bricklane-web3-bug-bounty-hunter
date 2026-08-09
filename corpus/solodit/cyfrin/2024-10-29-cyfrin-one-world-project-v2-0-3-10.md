---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: '`chainId` is used as the `EIP712Base::EIP712Domain.salt` in `DOMAIN_TYPEHASH`'
vuln_class: []
---

# `chainId` is used as the `EIP712Base::EIP712Domain.salt` in `DOMAIN_TYPEHASH`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `EIP712Base` implements EIP-712; however, there is a mistake in the definition of [`DOMAIN_TYPEHASH`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/EIP712Base.sol#L38) where `chainId` is used as the `salt` parameter.

According to the [EIP-712 specification](https://eips.ethereum.org/EIPS/eip-712#definition-of-domainseparator), the salt should only be used in the `DOMAN_TYPEHASH` as a last resort.

The `chainId` parameter should be used, but rather as a raw chain identifier as done in the OpenZeppelin [EIP-712](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/EIP712.sol#L37-L39) implementation:

```solidity
bytes32 private constant TYPE_HASH =
    keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)");
```

Consider changing the `DOMAIN_TYPEHASH` to use `chainId` instead of `salt`, or use the OpenZeppelin library directly.

**One World Project:** Intentional. Kept as it is.

**Cyfrin:** Acknowledged.
