---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Missing `DEPOSIT_WITNESS_TYPE_STRING` in `witnessHash`
vuln_class: []
---

# Missing `DEPOSIT_WITNESS_TYPE_STRING` in `witnessHash`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** `Escrow::deposit` computes `witnessHash` without the EIP-712 type hash, diverging from Permit2’s witness pattern. This breaks typed-struct binding and is inconsistent with how `reserve`, `release`, and `refund` hash their witnesses.

```solidity
// @audit missing the typehash
bytes32 witnessHash = keccak256(abi.encode(witness.requestId, witness.reserver, witness.releaser));
i_permit2.permitWitnessTransferFrom(
    permit, transferDetails, depositor, witnessHash, DEPOSIT_WITNESS_TYPE_STRING, signature
);
```

The [uniswap docs](https://docs.uniswap.org/contracts/permit2/reference/signature-transfer#single-permitwitnesstransferfrom) show how the `witnessHash` should be computed when calling `permitWitnessTransferFrom`:
> The witness that should be passed along with the permit message should be:
> ```solidity
>  bytes32 witness = keccak256(
>             abi.encode(_EXAMPLE_TRADE_TYPEHASH, exampleTrade.exampleTokenAddress, exampleTrade.exampleMinimumAmountOut));
> ```

**Impact:** Deposits signed with standard Permit2 witness tooling (which include the type hash) will fail verification, causing deposit DoS for correct clients.

**Recommended Mitigation:** Compute `witnessHash` using the EIP-712 hashStruct pattern, mirroring the Uniswap `permit2` docs and the other functions `reserve`, `release`, and `refund`:
```solidity
bytes32 witnessHash = keccak256(
    abi.encode(
        //keccak256(bytes(DEPOSIT_WITNESS_TYPE_STRING)),
        // put this into a constant then reference the constant
        bytes32(0x3829eef5438a5a932b2ec7bedc07110b7365b2ec8b814c211fd936d287c56b2a),
        witness.requestId,
        witness.reserver,
        witness.releaser
    )
);
```

**Atum:**
Fixed in commit [d304a6f](https://github.com/Atum-Labs/evm-contracts/commit/d304a6f5ac9ca282e7686a2396bfb789a11c343b).

**Cyfrin:** Verified.
