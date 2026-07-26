---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: State update performed after external call in `MembershipERC1155::mint`
vuln_class: []
---

# State update performed after external call in `MembershipERC1155::mint`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When `MembershipERC1155::mint` is invoked during a call to `MembershipFactory::joinDAO`, the `totalSupply` increment is performed after the call to `ERC1155::_mint`:

```solidity
function mint(address to, uint256 tokenId, uint256 amount) external override onlyRole(OWP_FACTORY_ROLE) {
    _mint(to, tokenId, amount, "");
    totalSupply += amount * 2 ** (6 - tokenId); // Update total supply with weight
}
```

While there does not appear to be any immediate impact, this is in violation of the Checks-Effects-Interactions (CEI) pattern and thus potentially unsafe due to the [invocation](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/49c0e4370d0cc50ea6090709e3835a3091e33ee2/contracts/token/ERC1155/ERC1155.sol#L285) of [`ERC1155::_doSafeTransferAcceptanceCheck`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/49c0e4370d0cc50ea6090709e3835a3091e33ee2/contracts/token/ERC1155/ERC1155.sol#L467-L486):

```solidity
if (to.isContract()) {
    try IERC1155Receiver(to).onERC1155Received(operator, from, id, amount, data) returns (bytes4 response) {
        if (response != IERC1155Receiver.onERC1155Received.selector) {
            revert("ERC1155: ERC1155Receiver rejected tokens");
        }
```

**Impact:** There does not appear to be any immediate impact, although any code executed within a receiver smart contract will work with an incorrect `totalSupply` state.

**Recommended Mitigation:** Consider increasing the `totalSupply` before the call to `_mint()`.

**One World Project:** Updated the pattern in [`30465a3`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/30465a3197adea883413298a9ac17fe8a1f0289e).

**Cyfrin:** Verified. State changes now done before external call is made.
