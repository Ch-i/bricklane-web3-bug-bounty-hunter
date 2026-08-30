---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-28-cyfrin-rocko-refinance-v2-0-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-28T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-28-cyfrin-rocko-refinance-v2-0
title: Refinancing reverts for `USDT` debt token
vuln_class: []
---

# Refinancing reverts for `USDT` debt token

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-28-cyfrin-rocko-refinance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-28-cyfrin-rocko-refinance-v2.0.md)_

---

**Description:** Refinancing reverts for `USDT` debt token due to the way protocol uses standard `IERC20::approve` and `transfer` functions.

**Impact:** Refinancing is bricked for `USDT` debt tokens. Marked as Low severity as officially only `USDC` is supported at this time. Note the implementation of `USDT` is different across chains; the protocol "as-is" would work with `USDT` on Base but not on Ethereum mainnet.

**Proof of Concept:** As part of the audit we have provided a fork fuzz testing suite; run this command: `forge test --fork-url ETH_RPC_URL --fork-block-number 22000000 --match-test test_FuzzRefinance_AaveToCompound_DepWeth_BorUsdt -vvv`

**Recommended Mitigation:** Replace all uses of `IERC20::approve` with [`SafeERC20::forceApprove`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L101-L108) and `IERC20::transfer` with `SafeERC20::safeTransfer` at L738, then re-run the PoC test and it now passes.

Ideally for added safety to prevent front-running of changes to existing approvals, use [`SafeERC20::safeIncreaseAllowance`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L68-L71) and [`safeDecreaseAllowance`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L82-L90) where suitable (for example in `_revokeTokenSpendApprovals` when the previous allowance amount is known could instead use `safeDecreaseAllowance`).

**Rocko:** Fixed in commit [751e906](https://github.com/getrocko/onchain/commit/751e906b7c2df6cb587e709b12de25593eb02c75).

**Cyfrin:** Verified.

\clearpage
