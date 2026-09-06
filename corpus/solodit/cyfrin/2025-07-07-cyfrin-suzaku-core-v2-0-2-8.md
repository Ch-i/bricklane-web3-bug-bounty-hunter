---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: '`NodeId` truncation can potentially cause validator registration denial of
  service'
vuln_class: []
---

# `NodeId` truncation can potentially cause validator registration denial of service

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** `AvalancheL1Middleware::addNode` function truncates 32-byte `nodeId` to 20-bytes when checking validator registration status. This truncation occurs when interacting with the `BalancerValidatorManager`.

```solidity
// AvalancheL1Middleware.sol
bytes32 valId = balancerValidatorManager.registeredValidators(
    abi.encodePacked(uint160(uint256(nodeId)))  // Truncates 32 bytes to 20 bytes
);
```

`uint160(uint256(nodeId))` discards the first 12 bytes of the `nodeId` before passing it to `BalancerValidatorManager::registeredValidators()`. However, the `ValidatorManager.registeredValidators()` function is designed to work with full bytes nodeId without any truncation.

**Impact:** Operators cannot register validators if another validator with a colliding truncated nodeId already exists

**Proof of Concept:** Run the following test in `AvalancheL1MiddlewareTest.t.sol`

```solidity
function test_NodeIdCollisionVulnerability() public {
    uint48 epoch = _calcAndWarpOneEpoch();

    // Create two different nodeIds that have the same first 20 bytes
    bytes32 nodeId1 = 0x0000000000000000000000001234567890abcdef1234567890abcdef12345678;
    bytes32 nodeId2 = 0xFFFFFFFFFFFFFFFFFFFFFFFF1234567890abcdef1234567890abcdef12345678;

    // share same first 20 bytes when truncated
    bytes memory truncated1 = abi.encodePacked(uint160(uint256(nodeId1)));
    bytes memory truncated2 = abi.encodePacked(uint160(uint256(nodeId2)));
    assertEq(keccak256(truncated1), keccak256(truncated2), "Truncated nodeIds should be identical");


    // Alice adds the first node
    vm.prank(alice);
    middleware.addNode(
                nodeId1,
                hex"ABABABAB", // dummy BLS
                uint64(block.timestamp + 2 days),
                PChainOwner({threshold: 1, addresses: new address[](1)}),
                PChainOwner({threshold: 1, addresses: new address[](1)}),
                100_000_000_001_000
            );

    // Verify first node was registered
    bytes32 validationId1 = mockValidatorManager.registeredValidators(truncated1);
    assertNotEq(validationId1, bytes32(0), "First node should be registered");

    // Alice tries to add the second node with different nodeId but same truncated bytes
    // This should fail due to collision
    vm.prank(alice);
    vm.expectRevert();
    middleware.addNode(
                nodeId2,
                hex"ABABABAB", // dummy BLS
                uint64(block.timestamp + 2 days),
                PChainOwner({threshold: 1, addresses: new address[](1)}),
                PChainOwner({threshold: 1, addresses: new address[](1)}),
                100_000_000_001_000
            );
}

```

**Recommended Mitigation:** Consider removing the forced truncation to 20 bytes


**Suzaku:**
Acknowledged.

**Cyfrin:** Acknowledged.
