---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-02-cyfrin-evo-soulboundtoken-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-06-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md
tags:
- firm:cyfrin
- report:2025-06-02-cyfrin-evo-soulboundtoken-v2-0
title: Use solady `safeTransferETH` to send eth
vuln_class: []
---

# Use solady `safeTransferETH` to send eth

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-02-cyfrin-evo-soulboundtoken-v2.0.md)_

---

**Description:** Using solady [`safeTransferETH`](https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L90-L98) is a [more efficient](https://github.com/devdacian/solidity-gas-optimization?tab=readme-ov-file#10-use-safetransferlibsafetransfereth-instead-of-solidity-call-effective-035-cheaper) way to send eth. Also since there is no point in leaving eth inside the contract, consider removing the `amountToWithdraw` input parameter and checks associated with it; instead just send the entire contract balance:
```solidity
function withdrawFees() external onlyOwner {
    uint256 amountToWithdraw = address(this).balance;
    if(amountToWithdraw > 0) {
        // from https://github.com/Vectorized/solady/blob/main/src/utils/SafeTransferLib.sol#L90-L98
        /// @solidity memory-safe-assembly
        assembly {
            if iszero(call(gas(), caller(), amountToWithdraw, codesize(), 0x00, codesize(), 0x00)) {
                mstore(0x00, 0xefde920d) // `SoulBoundToken__WithdrawFailed()`.
                revert(0x1c, 0x04)
            }
        }

        emit FeesWithdrawn(amountToWithdraw);
    }
}
```

Gas result:
```diff
{
- "withdrawFees": "13462"
+ "withdrawFees": "13353"
}
```

**Evo:**
Fixed in commit [b4fcadb](https://github.com/contractlevel/sbt/commit/b4fcadbd9c5684cc4e3b1ee3c39f72c406aaf658).

**Cyfrin:** Verified.

\clearpage
