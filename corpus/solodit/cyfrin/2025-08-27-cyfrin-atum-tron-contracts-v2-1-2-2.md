---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-27-cyfrin-atum-tron-contracts-v2-1-2-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-08-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md
tags:
- firm:cyfrin
- report:2025-08-27-cyfrin-atum-tron-contracts-v2-1
title: Incorrect description of `depositId` generation in `IEscrow`
vuln_class: []
---

# Incorrect description of `depositId` generation in `IEscrow`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-27-cyfrin-atum-tron-contracts-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-27-cyfrin-atum-tron-contracts-v2.1.md)_

---

**Description:** In `IEscrow.sol` file, it is mentioned that `depositId` is generated as the keccak256(signature), and this is incorrect. the depositId is generated using both `depositor` address and the `signature`

[IEscrow.sol#L207](https://github.com/Atum-Labs/tvm-contracts/blob/main/1-tvm-contracts/contracts/IEscrow.sol#L207)
```solidity
    /// @notice Deposit tokens into the escrow using Permit2 signature
>>  /// @dev The returned depositId is generated as keccak256(signature) and must be used for all subsequent operations
    /// @param permit Permit2 permit structure containing token, amount, nonce, and deadline
    /// @param depositor Address that owns the tokens and signed the permit
    /// @param witness Contains requestId (user reference) and authorized reserver/releaser addresses
    /// @param signature EIP-712 signature from depositor authorizing the transfer
    /// @return depositId Unique identifier for this deposit (keccak256(signature)) - use for reserve/release/refund
    function deposit( ... )
```


[Escrow.sol#L100-L102](https://github.com/Atum-Labs/tvm-contracts/blob/main/1-tvm-contracts/contracts/Escrow.sol#L100-L102)
```solidity
    function deposit( ... ) external whenNotPaused returns (bytes32 depositId) {
        ...

        // Generate a deposit ID from the depositor and signature
        // This prevents griefing attacks where a malicious depositor can use the signature of a legitimate deposit
>>      depositId = keccak256(abi.encode(depositor, signature));
        ...
    }
```

**Impact:**
- Incorrect docs leading to error in description of how the contract works

**Proof of Concept:** **Recommended Mitigation:**
correct the mistake by making it `generated as keccak256(depositor, signature)`

```diff
diff --git a/1-tvm-contracts/contracts/IEscrow.sol b/1-tvm-contracts/contracts/IEscrow.sol
index 914559a..9d21d99 100644
--- a/1-tvm-contracts/contracts/IEscrow.sol
+++ b/1-tvm-contracts/contracts/IEscrow.sol
@@ -204,7 +204,7 @@ interface IEscrow {
     // Core Functions

     /// @notice Deposit tokens into the escrow using Permit2 signature
-    /// @dev The returned depositId is generated as keccak256(signature) and must be used for all subsequent operations
+    /// @dev The returned depositId is generated as keccak256(depositor, signature) and must be used for all subsequent operations
     /// @param permit Permit2 permit structure containing token, amount, nonce, and deadline
     /// @param depositor Address that owns the tokens and signed the permit
     /// @param witness Contains requestId (user reference) and authorized reserver/releaser addresses
```

**Atum:**
Fixed in commit [0772f28](https://github.com/Atum-Labs/tvm-contracts/commit/0772f285435f65900b74cd8b9cbc6cddec079dbd) for `tvm-contracts` and [f668872](https://github.com/Atum-Labs/evm-contracts/commit/f668872b0aa6b8724eff0c03af5a45bc66788067) for `evm-contracts`.

**Cyfrin:** Verified.

\clearpage
