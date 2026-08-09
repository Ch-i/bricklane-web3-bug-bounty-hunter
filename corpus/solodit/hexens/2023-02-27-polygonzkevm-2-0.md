---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 7. DISCREPANCY IN TRANSACTION RLP DECODING BETWEEN ZKEVM AND EVM
vuln_class: []
---

# 7. DISCREPANCY IN TRANSACTION RLP DECODING BETWEEN ZKEVM AND EVM

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Low

**Path:** [StakeableVestingFactory.sol:deployStakeableVesting#L39-L71](https://github.com/0xPolygonHermez/zkevm-rom/blob/develop/main/load-tx-rlp.zkasm#L164-L206)

**Description:**

In the load-tx-rlp.zkasm implementation of transaction RLP decoding the code label dataREAD stands for the part of decoding the DATA field of the transaction. The data field is encoded as an RLP string and can be of both short and long size, as the RLP format states (https://ethereum.org/en/developers/docs/data-structures-and-encoding/rlp#definition) the string can be represented in two ways based on the length (0-55 bytes and 55+ bytes):

-   …

-   Otherwise, if a string is 0-55 bytes long, the RLP encoding consists of a single byte with value 0x80 (dec. 128) plus the length of the string followed by the string. The range of the first byte is thus [0x80, 0xb7] (dec. [128, 183]).

-   If a string is more than 55 bytes long, the RLP encoding consists of a single byte with value 0xb7 (dec. 183) plus the length in bytes of the length of the string in binary form, followed by the length of the string, followed by the string. For example, a 1024 byte long string would be encoded as \xb9\x04\x00 (dec. 185, 4, 0) followed by the string. Here, 0xb9 (183 + 2 = 185) as the first byte, followed by the 2 bytes 0x0400 (dec. 1024) that denote the length of the actual string. The range of the first byte is thus [0xb8, 0xbf] (dec. [184, 191]).
- …


The problem arises when one wants to construct an RLP transaction with a short data field (less than 55 bytes) but encode it in long string format (0xb801AA = [“AA“], example of 1 byte string but in long string format). The EVM has these checks implemented to avoid such situations:
https://github.com/ethereum/go-ethereum/blob/master/rlp/decode.go#L1008-L1011 and consequently, as the zkEVM-node inherits the lib, it has the checks as well.

However, the zkEVM ROM’s RLP decoding mechanism fails to check these cases (both for short/long strings and short/long lists).

A guaranteed impact is that the batch sequencing mechanism will be blocked and broken because of this “poison” transaction. Possible steps will be:

1. The attacker forces a batch with wrongful RLP encoding

2. The trusted sequencer either sequences it or ignores and the timeout period passes

3. The trusted sequencer or the attacker sequences the forced batch

4. The attacker verifies the batch as it is fully provable by the zkEVM ROM and claims from the bridge or uses the assets which were transferred by the poison transaction

5. The zkEVM network halts as synchronizers cannot sync with the forced batch, and the network stays desynced

6. The possible response steps to the situation:

   1.  Fix the RLP decoding in the zkEVM ROM and rollback the state in L1 by redeploying the Proof-of-Efficiency contract with older state roots

   2.  Change the RLP decoding to a wrongful one in the nodes and push an update for the network with incorrect RLP

As the most probable scenario is to go with 6.a solution, rather than not actually fixing the bug and introducing a new one in the nodes (6.b), the situation will favour the attacker as after the rollback, there will be possible to basically double spend the assets.

```
dataREAD:
        $ => D                          :MLOAD(batchHashPos)
        D                               :MSTORE(dataStarts)
        1 => D
        %CALLDATA_OFFSET => SP          :CALL(addHashTx)
                                        :CALL(addBatchHashData)
        A - 0x80                        :JMPN(veryShortData)
        A - 0x81                        :JMPN(endData)
        A - 0xb8                        :JMPN(shortData)
        A - 0xc0                        :JMPN(longData, invalidTxRLP)

veryShortData:
        1                               :MSTORE(txCalldataLen)
        31 => D                         :CALL(SHLarith)
        A                               :MSTORE(SP++), JMP(endData)

shortData:
        $ => D                          :MLOAD(batchHashPos)
        D                               :MSTORE(dataStarts)
        A - 0x80 => B                   :MSTORE(txCalldataLen), JMP(readData)

longData:
        A - 0xb7 => D                   :CALL(addHashTx)
                                        :CALL(addBatchHashData)
        $ => D                          :MLOAD(batchHashPos)
        D                               :MSTORE(dataStarts)
        A => B                          :MSTORE(txCalldataLen)

readData:
        ; check binaries
        32 => D
        B - D                           :JMPN(readDataFinal)
        B - D                           :MSTORE(txDataRead), CALL(addHashTx)
        A                               :MSTORE(SP++), CALL(addBatchHashByteByByte)
        $ => B                          :MLOAD(txDataRead), JMP(readData)

readDataFinal:
        B - 1                           :JMPN(endData)
        B => D                          :CALL(addHashTx)
        32 - D => D                     :CALL(SHLarith)
        A                               :MSTORE(SP)
        32 - D => D                     :CALL(addBatchHashByteByByte)

```
*Evm*
```
case b < 0xC0:
   // If a string is more than 55 bytes long, the RLP encoding consists of a
   // single byte with value 0xB7 plus the length of the length of the
   // string in binary form, followed by the length of the string, followed
   // by the string. For example, a length-1024 string would be encoded as
   // 0xB90400 followed by the string. The range of the first byte is thus
   // [0xB8, 0xBF].
   size, err = s.readUint(b - 0xB7)
   if err == nil && size < 56 {
       err = ErrCanonSize
   }
   return String, size, err

```

**Remediation:** Add checks for string and list decoding to ensure that long-format encoding is done for sizes more than 55 bytes.

**Status:** Fixed

- - -
