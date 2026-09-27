---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-14-cyfrin-atum-evm-contracts-v2-0-2-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-08-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-14-cyfrin-atum-evm-contracts-v2-0
title: Incorrect `witnessTypeString` in `Escow::deposit` passed to `SignatureTransfer::permitWitnessTransferFrom`
vuln_class: []
---

# Incorrect `witnessTypeString` in `Escow::deposit` passed to `SignatureTransfer::permitWitnessTransferFrom`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-14-cyfrin-atum-evm-contracts-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-14-cyfrin-atum-evm-contracts-v2.0.md)_

---

**Description:** [Uniswap docs](https://docs.uniswap.org/contracts/permit2/reference/signature-transfer#single-permitwitnesstransferfrom) state `witnessTypeString` passed to `SignatureTransfer::permitWitnessTransferFrom` should include `TokenPermissions ` in the typehash:

> And the witnessTypeString to be passed in should be:
> ```solidity
> string constant witnessTypeString = "ExampleTrade witness)ExampleTrade(address exampleTokenAddress,uint256 exampleMinimumAmountOut)TokenPermissions(address token,uint256 amount)"
> ```

But `Escrow::deposit` doesn't do this:
```solidity
string private constant DEPOSIT_WITNESS_TYPE_STRING =
        "DepositWitness(bytes32 requestId,address reserver,address releaser)";

i_permit2.permitWitnessTransferFrom(
    permit, transferDetails, depositor, witnessHash, DEPOSIT_WITNESS_TYPE_STRING, signature
);
```

**Impact:** Deposit DoS for otherwise valid signatures if the client’s `witnessTypeString` differs. There is also a ecosystem integration risk: minor deviations by third-party signers break deposits even though witness values match.

**Recommended Mitigation:** Add another constant for the "full" deposit witness type string then pass that as the `witnessTypeString` when calling `SignatureTransfer::permitWitnessTransferFrom`:
```solidity
string private constant FULL_DEPOSIT_WITNESS_TYPE_STRING =
        "DepositWitness witness)DepositWitness(bytes32 requestId,address reserver,address releaser)TokenPermissions(address token,uint256 amount)";

i_permit2.permitWitnessTransferFrom(
    permit, transferDetails, depositor, witnessHash, FULL_DEPOSIT_WITNESS_TYPE_STRING, signature
);
```

**Atum:**
Fixed in commit [d304a6f](https://github.com/Atum-Labs/evm-contracts/commit/d304a6f5ac9ca282e7686a2396bfb789a11c343b).

**Cyfrin:** Verified.

\clearpage
