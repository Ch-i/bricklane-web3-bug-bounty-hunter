---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0-2-6
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-securitize-public-stock-ramp-v2-0
title: Unused nonce Field in `ExecutePreApprovedTransaction` struct
vuln_class: []
---

# Unused nonce Field in `ExecutePreApprovedTransaction` struct

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md)_

---

**Description:** The `ExecutePreApprovedTransaction` struct contains a nonce field that is never used or validated:

```solidity
   /**
     * @dev Tx type - EIP712
     */
    struct ExecutePreApprovedTransaction {
        string senderInvestor;
        address destination;
        bytes data;
        uint256 nonce;
    }
```
In `SecuritizeOnRamp::executePreApprovedTransaction`, the `txData.nonce` value passed by the caller is completely ignored. The function uses the internal `noncePerInvestor` mapping instead:

```solidity
 function hashTx(ExecutePreApprovedTransaction calldata txData) private view returns (bytes32) {
        bytes32 structHash = keccak256(
            abi.encode(
                TXTYPE_HASH,
                keccak256(bytes(txData.senderInvestor)),
                txData.destination,
                keccak256(txData.data),
                noncePerInvestor[txData.senderInvestor]
            )
        );

        return _hashTypedDataV4(structHash);
    }
```

This creates dead code and a confusing API where callers must include a nonce value in their transaction data that has no effect on execution.

**Recommended Mitigation:** Remove the unused nonce field from the struct.

**Securitize:** Acknowledged for now to avoid breaking backend changes.
