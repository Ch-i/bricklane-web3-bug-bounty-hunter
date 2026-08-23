---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-1-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Wrong value is returned in `upperLookupRecentCheckpoint`
vuln_class: []
---

# Wrong value is returned in `upperLookupRecentCheckpoint`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** In `Checkpoint::upperLookupRecentCheckpoint`  function is designed to check if there exists a checkpoint with a key less than or equal to the provided search key in the structure (i.e., the structure is not empty). If such a checkpoint exists, it returns the key, value, and position of the checkpoint in the trace.
However, the function behaves incorrectly when a valid hint is provided, which contradicts its intended purpose.

This comes from the fact that `at` is returning the correct value.

```solidity
function at(Trace256 storage self, uint32 pos) internal view returns (Checkpoint256 memory) {
        OZCheckpoints.Checkpoint208 memory checkpoint = self._trace.at(pos);
        return Checkpoint256({_key: checkpoint._key, _value: self._values[checkpoint._value]});
    }
```

**Impact:** The incorrect handling of the checkpoint value in `upperLookupRecentCheckpoint` can cause the function to revert or return an incorrect value, undermining the reliability of the checkpoint lookup mechanism.

**Proof of Concept:** Run the following test

```solidity
contract CheckpointsBugTest is Test {
    using ExtendedCheckpoints for ExtendedCheckpoints.Trace256;

    ExtendedCheckpoints.Trace256 internal trace;

    function setUp() public {
        // Initialize the trace with some checkpoints
        trace.push(100, 1000); // timestamp 100, value 1000
        trace.push(200, 2000); // timestamp 200, value 2000
        trace.push(300, 3000); // timestamp 300, value 3000
    }

    function test_upperLookupRecentCheckpoint_withoutHint_works() public view {
        // Test without hint - this should work correctly
        (bool exists, uint48 key, uint256 value, uint32 pos) = trace.upperLookupRecentCheckpoint(150);

        assertTrue(exists, "Checkpoint should exist");
        assertEq(key, 100, "Key should be 100");
        assertEq(value, 1000, "Value should be 1000");
        assertEq(pos, 0, "Position should be 0");
    }

    // This test demonstrates the bug when using a valid hint
    function test_upperLookupRecentCheckpoint_withValidHint_demonstratesBug() public {

        // First, let's get the correct hint (position 0)
        uint32 validHint = 0;
        bytes memory hintBytes = abi.encode(validHint);

        // Call with hint - this will fail due to the bug
        vm.expectRevert(); // Expecting a revert due to array bounds error
        trace.upperLookupRecentCheckpoint(150, hintBytes);
    }

}
```

**Recommended Mitigation:** Modify the `upperLookupRecentCheckpoint` function to directly use the `checkpoint._value` returned by the at function, rather than referencing `self._values[checkpoint._value]`. The proposed change is as follows:

```diff
function upperLookupRecentCheckpoint(
        Trace256 storage self,
        uint48 key,
        bytes memory hint_
    ) internal view returns (bool, uint48, uint256, uint32) {
        if (hint_.length == 0) {
            return upperLookupRecentCheckpoint(self, key);
        }
        uint32 hint = abi.decode(hint_, (uint32));
        Checkpoint256 memory checkpoint = at(self, hint);
        if (checkpoint._key == key) {
-           return (true, checkpoint._key, self._values[checkpoint._value], hint);
+           return (true, checkpoint._key, checkpoint._value, hint);
        }
        if (checkpoint._key < key && (hint == length(self) - 1 || at(self, hint + 1)._key > key)) {
-            return (true, checkpoint._key, self._values[checkpoint._value], hint);
+            return (true, checkpoint._key, checkpoint._value, hint);
        }
        return upperLookupRecentCheckpoint(self, key);
```

**Suzaku:**
Fixed in commit [d198969](https://github.com/suzaku-network/suzaku-core/pull/155/commits/d198969910088d087cd52d2a6bad15fe2530df9c).

**Cyfrin:** Verified.
