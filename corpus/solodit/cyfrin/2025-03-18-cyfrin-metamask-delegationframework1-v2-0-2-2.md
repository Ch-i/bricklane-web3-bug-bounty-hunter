---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-18-cyfrin-metamask-delegationframework1-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-18-cyfrin-metamask-delegationframework1-v2-0
title: NFT safe transfers will revert using `ERC721TransferEnforcer`
vuln_class: []
---

# NFT safe transfers will revert using `ERC721TransferEnforcer`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-18-cyfrin-Metamask-DelegationFramework1-v2.0.md)_

---

**Description:** The `ERC721TransferEnforcer` enforcer is designed to authorize NFT token transfers, but it currently restricts transfers to only use the `transferFrom` selector. The issue lies in this code section:

```solidity
//ERC721TransferEnforcer.sol
bytes4 selector_ = bytes4(callData_[0:4]);

if (target_ != permittedContract_) {
    revert("ERC721TransferEnforcer:unauthorized-contract-target");
} else if (selector_ != IERC721.transferFrom.selector) {
    revert("ERC721TransferEnforcer:unauthorized-selector");
} else if (transferTokenId_ != permittedTokenId_) {
    revert("ERC721TransferEnforcer:unauthorized-token-id");
}
```

The ERC721 standard includes multiple transfer methods:

`transferFrom(address from, address to, uint256 tokenId)`
`safeTransferFrom(address from, address to, uint256 tokenId)`
`safeTransferFrom(address from, address to, uint256 tokenId, bytes data)`

The enforcer currently only supports the `transferFrom` method, which doesn't perform receiver capability checks. The `safeTransferFrom` methods are crucial for safely transferring NFTs to contracts, as they check whether the receiving contract supports the ERC721 standard through the onERC721Received callback.


**Impact:** Users are unable to utilize safer NFT transfer methods when using this enforcer.


**Recommended Mitigation:** Consider modifying the `ERC721TransferEnforcer` to accept all valid ERC721 transfer selectors.

**Metamask:** Fixed in [1a0ff2d](https://github.com/MetaMask/delegation-framework/commit/1a0ff2d92162f61945154d0a56a52b5878a2c9d0).

**Cyfrin:** Resolved.
