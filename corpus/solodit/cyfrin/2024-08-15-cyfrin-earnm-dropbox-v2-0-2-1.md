---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use inheritance order from most "base-like" to "most-derived" so `super` will
  call correct parent function in `DropBox::supportsInterface`
vuln_class: []
---

# Use inheritance order from most "base-like" to "most-derived" so `super` will call correct parent function in `DropBox::supportsInterface`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Use inheritance order from most "base-like" to "most-derived"; this is considered good practice and can be important since Solidity [searches](https://solidity-by-example.org/inheritance/) for parent functions from right to left.

`DropBox` inherits and overrides the following function from two different parent contracts and calls `super`:
```solidity
  function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721C, ERC2981) returns (bool) {
    return super.supportsInterface(interfaceId);
  }
```

The current ordering is:
```solidity
contract DropBox is OwnableBasic, ERC721C, BasicRoyalties, ReentrancyGuard, DropBoxFractalProtocol, IVRFHandlerReceiver {
```

As Solidity searches from right to left, this will bypass `ERC721C::supportsInterface` and instead execute `ERC2981::supportsInterface` since `BasicRoyalties` appears after `ERC721C` in the inheritance order.

`ERC2981::supportsInterface` ends up [executing](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/common/ERC2981.sol#L22-L55) `ERC165::supportsInterface` but `ERC721C::supportsInterface` explicitly intends to override `ERC165::supportsInterface`:
```solidity
    /**
     * @notice Indicates whether the contract implements the specified interface.
     * @dev Overrides supportsInterface in ERC165.
     * @param interfaceId The interface id
     * @return true if the contract implements the specified interface, false otherwise
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
        return
        interfaceId == type(ICreatorToken).interfaceId ||
        interfaceId == type(ICreatorTokenLegacy).interfaceId ||
        super.supportsInterface(interfaceId);
    }
```

Hence due to the current inheritance order `DropBox::supportsInterface` will bypass `ERC721C::supportsInterface` to execute `ERC2981::supportsInterface`  and `ERC165::supportsInterface` which appears to be incorrect.

**Recommended Mitigation:** File: `DropBox.sol`:
```diff
- contract DropBox is OwnableBasic, ERC721C, BasicRoyalties, ReentrancyGuard, DropBoxFractalProtocol, IVRFHandlerReceiver {
+ contract DropBox is IVRFHandlerReceiver, DropBoxFractalProtocol, ReentrancyGuard, OwnableBasic, BasicRoyalties, ERC721C {

  function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721C, ERC2981) returns (bool) {
-    return super.supportsInterface(interfaceId);
// @audit make it explicit which parent function to call
+   return ERC721C.supportsInterface(interfaceId);
  }
```

File: `VRFHandler.sol`:
```diff
- contract VRFHandler is VRFConsumerBaseV2Plus, IVRFHandler {
+ contract VRFHandler is IVRFHandler, VRFConsumerBaseV2Plus {
```

**Mode:**
Fixed in commit [c66de99](https://github.com/Earnft/dropbox-smart-contracts/commit/c66de99a6776bfb5198bee90d7a9c139ec08fc5f).

**Cyfrin:** Verified.

\clearpage
