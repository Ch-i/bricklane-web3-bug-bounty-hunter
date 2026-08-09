---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Potentially dangerous out-of-bounds memory access in `BytesParsing::sliceUnchecked`
vuln_class: []
---

# Potentially dangerous out-of-bounds memory access in `BytesParsing::sliceUnchecked`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

**Description:** [`BytesParsing::sliceUnchecked`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/libraries/BytesParsing.sol#L16-L57) currently[ bails early](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/libraries/BytesParsing.sol#L21-L24) for the degenerate case when the slice length is zero; however, there is no validation on the length of the encoded bytes parameter `encoded` itself. If the length of `encoded` is less than the slice `length`, then it is possible to access memory out-of-bounds.

```solidity
function sliceUnchecked(bytes memory encoded, uint256 offset, uint256 length)
    internal
    pure
    returns (bytes memory ret, uint256 nextOffset)
{
    //bail early for degenerate case
    if (length == 0) {
        return (new bytes(0), offset);
    }

    assembly ("memory-safe") {
        nextOffset := add(offset, length)
        ret := mload(freeMemoryPtr)

        /* snip: inline dev comments */

        let shift := and(length, 31) //equivalent to `mod(length, 32)` but 2 gas cheaper
        if iszero(shift) { shift := wordSize }

        let dest := add(ret, shift)
        let end := add(dest, length)
        for { let src := add(add(encoded, shift), offset) } lt(dest, end) {
            src := add(src, wordSize)
            dest := add(dest, wordSize)
        } { mstore(dest, mload(src)) }

        mstore(ret, length)
        //When compiling with --via-ir then normally allocated memory (i.e. via new) will have 32 byte
        //  memory alignment and so we enforce the same memory alignment here.
        mstore(freeMemoryPtr, and(add(dest, 31), not(31)))
    }
}
```

Since the `for` loop begins at the offset of `encoded` in memory, accounting for its length and accompanying `shift` calculation depending on the `length` supplied, and execution continues so long as `dest` is less than `end`, it is possible to continue loading additional words out of bounds simply by passing larger `length` values. Therefore, regardless of the length of the original bytes, the output slice will always have a size defined by the `length` parameter.

It is understood that this is known behavior due to the unchecked nature of this function and the accompanying checked version, which performs validation on the `nextOffset` return value compared with the length of the encoded bytes.

```solidity
function slice(bytes memory encoded, uint256 offset, uint256 length)
    internal
    pure
    returns (bytes memory ret, uint256 nextOffset)
{
    (ret, nextOffset) = sliceUnchecked(encoded, offset, length);
    checkBound(nextOffset, encoded.length);
}
```

It has not been possible within the constraints of this review to identify a valid scenario in which malicious calldata can make use of this behavior to launch a successful exploit; however, this is not a guarantee that the usage of this library function is bug-free since there do [exist](https://solodit.xyz/issues/h-04-incorrect-implementation-of-access-control-in-mimoproxyexecute-code4rena-mimo-defi-mimo-august-2022-contest-git) [certain](https://solodit.xyz/issues/m-2-high-risk-checks-can-be-bypassed-with-extra-calldata-padding-sherlock-olympus-on-chain-governance-git) [quirks](https://solodit.xyz/issues/opcalldataload-opcalldatacopy-reading-position-out-of-calldata-bounds-spearbit-none-polygon-zkevm-pdf) related to the loading of calldata.

**Impact:** The impact is limited in the context of the library function's usage in the scope of this review; however, it is advisable to check any other usage elsewhere and in the future to ensure that this behavior cannot be weaponized. `BytesParsing::sliceUnchecked` is currently only used in [`WormholeCctpMessages::_decodeBytes`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/libraries/WormholeCctpMessages.sol#L227-L235), which itself is called in [`WormholeCctpMessages::decodeDeposit`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/libraries/WormholeCctpMessages.sol#L196-L223). This latter function is utilized in two places:
1. [`Logic::decodeDepositWithPayload`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/CircleIntegration/Logic.sol#L126-L148): here, any issues in slicing the encoded bytes would impact users' ability to decode payloads, potentially stopping them from correctly retrieving the necessary information for redemptions.
2. [`WormholeCctpTokenMessenger::verifyVaaAndMint`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/WormholeCctpTokenMessenger.sol#L144-L197)/[`WormholeCctpTokenMessenger::verifyVaaAndMintLegacy`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/WormholeCctpTokenMessenger.sol#L199-L253): these functions verify and reconcile CCTP and Wormhole messages in order to mint tokens for the encoded mint recipient. Fortunately, for a malicious calldata payload, Wormhole itself will revert when [`IWormhole::parseAndVerifyVM`](https://github.com/wormhole-foundation/wormhole/blob/eee4641f55954d2d0db47831688a2e97eb20f7ee/ethereum/contracts/Messages.sol#L15-L20) is called via [`WormholeCctpTokenMessenger::_parseAndVerifyVaa`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/f7df33b159a71b163b8b5c7e7381c0d8f193da99/evm/src/contracts/WormholeCctpTokenMessenger.sol#L295-L311) since it will be unable to [retrieve a valid version number](https://github.com/wormhole-foundation/wormhole/blob/main/ethereum/contracts/Messages.sol#L150) when [casting](https://github.com/wormhole-foundation/wormhole/blob/main/ethereum/contracts/libraries/external/BytesLib.sol#L309) to `uint8`.

**Proof of Concept:** Apply the following git diff to differential test against a Python implementation:
```diff
diff --git a/evm/.gitignore b/evm/.gitignore
--- a/evm/.gitignore
+++ b/evm/.gitignore
@@ -7,3 +7,4 @@ lib
 node_modules
 out
 ts/src/ethers-contracts
+venv/
diff --git a/evm/forge/tests/differential/BytesParsing.t.sol b/evm/forge/tests/differential/BytesParsing.t.sol
new file mode 100644
--- /dev/null
+++ b/evm/forge/tests/differential/BytesParsing.t.sol
@@ -0,0 +1,72 @@
+// SPDX-License-Identifier: Apache 2
+pragma solidity ^0.8.19;
+
+import "forge-std/Test.sol";
+import "forge-std/console.sol";
+
+import {BytesParsing} from "src/libraries/BytesParsing.sol";
+
+contract BytesParsingTest is Test {
+    using BytesParsing for bytes;
+
+    function setUp() public {}
+
+    function test_sliceUncheckedFuzz(bytes memory encoded, uint256 offset, uint256 length) public {
+        bound(offset, 0, type(uint8).max);
+        bound(length, 0, type(uint8).max);
+        if (offset > encoded.length || length > encoded.length || offset + length > encoded.length) {
+            return;
+        }
+
+        sliceUncheckedBase(encoded, offset, length);
+    }
+
+    function test_sliceUncheckedConcreteReadOOB() public {
+        bytes memory encoded = bytes("");
+        bytes32 dirty = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef;
+        assembly {
+            mstore(add(encoded, 0x20), dirty)
+        }
+        uint256 offset = 0;
+        uint256 length = 32;
+
+        sliceUncheckedBase(encoded, offset, length);
+    }
+
+    function sliceUncheckedBase(bytes memory encoded, uint256 offset, uint256 length)
+        internal
+        returns (
+            bytes memory soliditySlice,
+            uint256 solidityNextOffset,
+            bytes memory pythonSlice,
+            uint256 pythonNextOffset
+        )
+    {
+        (soliditySlice, solidityNextOffset) = encoded.sliceUnchecked(offset, length);
+        assertEq(soliditySlice.length, length, "wrong length");
+
+        string[] memory inputs = new string[](9);
+        inputs[0] = "python";
+        inputs[1] = "forge/tests/differential/python/bytes_parsing.py";
+        inputs[2] = "slice_unchecked";
+        inputs[3] = "--encoded";
+        inputs[4] = vm.toString(encoded);
+        inputs[5] = "--offset";
+        inputs[6] = vm.toString(offset);
+        inputs[7] = "--length";
+        inputs[8] = vm.toString(length);
+
+        (pythonSlice, pythonNextOffset) = abi.decode(vm.ffi(inputs), (bytes, uint256));
+
+        emit log_named_uint("soliditySlice.length", soliditySlice.length);
+        emit log_named_uint("pythonSlice.length", pythonSlice.length);
+
+        emit log_named_bytes("soliditySlice", soliditySlice);
+        emit log_named_bytes("pythonSlice", pythonSlice);
+        emit log_named_uint("solidityNextOffset", solidityNextOffset);
+        emit log_named_uint("pythonNextOffset", pythonNextOffset);
+
+        assertEq(soliditySlice, pythonSlice, "wrong slice");
+        assertEq(solidityNextOffset, pythonNextOffset, "wrong next offset");
+    }
+}
diff --git a/evm/forge/tests/differential/python/bytes_parsing.py b/evm/forge/tests/differential/python/bytes_parsing.py
new file mode 100644
--- /dev/null
+++ b/evm/forge/tests/differential/python/bytes_parsing.py
@@ -0,0 +1,42 @@
+from eth_abi import encode
+import argparse
+
+
+def main(args):
+    if args.function == "slice_unchecked":
+        slice, next_offset = slice_unchecked(args)
+        encode_and_print(slice, next_offset)
+
+
+def slice_unchecked(args):
+    if args.length == 0:
+        return (b"", args.offset)
+
+    next_offset = args.offset + args.length
+
+    encoded_bytes = (
+        bytes.fromhex(args.encoded[2:])
+        if args.encoded.startswith("0x")
+        else bytes.fromhex(args.encoded)
+    )
+    return (encoded_bytes[args.offset : next_offset], next_offset)
+
+
+def encode_and_print(slice, next_offset):
+    encoded_output = encode(["bytes", "uint256"], (slice, next_offset))
+    ## append 0x for FFI parsing
+    print("0x" + encoded_output.hex())
+
+
+def parse_args():
+    parser = argparse.ArgumentParser()
+    parser.add_argument("function", choices=["slice_unchecked"])
+    parser.add_argument("--encoded", type=str)
+    parser.add_argument("--offset", type=int)
+    parser.add_argument("--length", type=int)
+    return parser.parse_args()
+
+
+if __name__ == "__main__":
+    args = parse_args()
+    main(args)
diff --git a/evm/forge/tests/differential/python/requirements.txt b/evm/forge/tests/differential/python/requirements.txt
new file mode 100644
--- /dev/null
+++ b/evm/forge/tests/differential/python/requirements.txt
@@ -0,0 +1 @@
+eth_abi==5.0.0
\ No newline at end of file
diff --git a/evm/foundry.toml b/evm/foundry.toml
--- a/evm/foundry.toml
+++ b/evm/foundry.toml
@@ -31,4 +31,7 @@ gas_reports = ["*"]

 gas_limit = "18446744073709551615"

+[profile.ffi]
+ffi = true
+
```

**Recommended Mitigation:** Consider bailing early if the length of the bytes from which to construct a slice is zero, and always ensure the resultant offset is correctly validated against the length when using the unchecked version of the function.

**Wormhole Foundation:** The [slice method](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/7599cbe984ce17dd9e87c81fb0b6ea12ff1635ba/evm/src/libraries/BytesParsing.sol#L59) does this checking for us. Since we’re controlling the length specified in the wire format, we can safely use the unchecked variant.

**Cyfrin:** Acknowledged.
