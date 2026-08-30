---
affected_contracts: []
derives_from: []
id: solodit-hexens-2023-02-27-polygonzkevm-2-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-02-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
tags:
- firm:hexens
- report:2023-02-27-polygonzkevm
title: 8. GASLIMIT AND CHAINID MAX SIZE DIFFERENCE BETWEEN ZKEVM AND EVM
vuln_class: []
---

# 8. GASLIMIT AND CHAINID MAX SIZE DIFFERENCE BETWEEN ZKEVM AND EVM

_Section severity (from Solodit section header): Low_  
_Audit firm: Hexens_  
_Source report: [2023-02-27-PolygonZkEvm.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md)_

---

**Severity:** Low

**Path:** [StakeableVestingFactory.sol:deployStakeableVesting:L39-71](https://github.com/0xPolygonHermez/zkevm-rom/blob/develop/main/load-tx-rlp.zkasm)

**Description:** 

There is a difference between the transaction’s gas limit and chain id max sizes between zkEVM and EVM implementations.
In https://github.com/0xPolygonHermez/zkevm-rom/blob/develop/main/load-tx-rlp.zkasm GasLimit’s maximal size is defined as 256 bit and ChainID’s 64 bit.
The EVM sizes are:
Gas limit’s maximal size is 64 bit https://github.com/ethereum/go-ethereum/blob/79a478bb6176425c2400e949890e668a3d9a3d05/core/types/tx_legacy.go#L29 and ChainID’s maximal size is 256 bit 
https://github.com/ethereum/go-ethereum/blob/01808421e20ba9d19c029b64fcda841df77c9aff/core/types/transaction.go#L75

A possible impact is we can create a transaction with the correct chainID but encoded as a larger uint which is acceptable by zkEVM nod as well as EVM (RLP lib), but it will be impossible to prove a batch including that transaction. Given the fact that the zkASM EVM will be failing in the load-rlp stage, the batch will be discarded, and also the fact that there is a possibility to freely spam these kinds of transactions to the sequencer, it will be possible to stop the network availability. 
*zkASM ROM:*

```
;; Read RLP 'gas limit'
       ; 256 bits max
gasLimitREAD:
       1 => D                          :CALL(addHashTx)
                                       :CALL(addBatchHashData)
       A - 0x80                        :JMPN(endGasLimit)
       A - 0x81                        :JMPN(gasLimit0)
       A - 0xa1                        :JMPN(shortGasLimit, invalidTxRLP)
```
```
;; Read RLP 'chainId'
       ; 64 bits max
chainREAD:
       1 => D                          :CALL(addHashTx)
                                       :CALL(addBatchHashData)
       A - 0x80                        :JMPN(endChainId)
       A - 0x81                        :JMPN(chainId0)
       A - 0x89                        :JMPN(shortChainId, invalidTxRLP)
```
*EVM Transaction:*
```
// LegacyTx is the transaction data of regular Ethereum transactions.
type LegacyTx struct {
   Nonce    uint64          // nonce of sender account
   GasPrice *big.Int        // wei per gas
   Gas      uint64          // gas limit
   To       *common.Address `rlp:"nil"` // nil means contract creation
   Value    *big.Int        // wei amount
   Data     []byte          // contract invocation input data
   V, R, S  *big.Int        // signature values
}
```
```
// TxData is the underlying data of a transaction.
//
// This is implemented by DynamicFeeTx, LegacyTx and AccessListTx.
type TxData interface {
   txType() byte // returns the type ID
   copy() TxData // creates a deep copy and initializes all fields

   chainID() *big.Int
   accessList() AccessList
   data() []byte
   gas() uint64
   gasPrice() *big.Int
   gasTipCap() *big.Int
   gasFeeCap() *big.Int
   value() *big.Int
   nonce() uint64
   to() *common.Address

   rawSignatureValues() (v, r, s *big.Int)
   setSignatureValues(chainID, v, r, s *big.Int)
}
```
**Remediation:** Change Gas Limit and Chain ID RLP decoding according to the EVM’s Gas Limit and Chain ID max sizes.  

**Status:** Fixed

- - -
