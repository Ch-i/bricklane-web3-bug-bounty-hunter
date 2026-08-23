---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: '`KarmaNFT.sol` incorrectly simulates minting event'
vuln_class: []
---

# `KarmaNFT.sol` incorrectly simulates minting event

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** It emits Transfer event to simulate minting:
```solidity
    /**
     * @notice Emits transfer event to simulate minting an NFT to the caller's address.
     */
    function mint() external {
        emit Transfer(msg.sender, msg.sender, uint256(uint160(msg.sender)));
    }
```
EIP-721 specifies that when NFT is created, it uses `from = address(0)` https://eips.ethereum.org/EIPS/eip-721#specification:
> /// @dev This emits when ownership of any NFT changes by any mechanism.
    ///  This event emits when NFTs are created (`from` == 0) and destroyed
    ///  (`to` == 0). Exception: during contract creation, any number of NFTs
    ///  may be created and assigned without emitting Transfer. At the time of
    ///  any transfer, the approved address for that NFT (if any) is reset to none.
    event Transfer(address indexed _from, address indexed _to, uint256 indexed _tokenId);

**Impact:** Incorrect event is emitted.

**Recommended Mitigation:**
```diff
    function mint() external {
-       emit Transfer(msg.sender, msg.sender, uint256(uint160(msg.sender)));
+       emit Transfer(address(0), msg.sender, uint256(uint160(msg.sender)));
    }

```

**StatusL2:** Fixed in [72cd30d](https://github.com/status-im/status-network-monorepo/commit/72cd30d61a02aa85c11f1bd460e07e047e855333).

**Cyfrin:** Verified.
