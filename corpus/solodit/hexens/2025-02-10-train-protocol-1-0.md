---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-10-train-protocol-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-02-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md
tags:
- firm:hexens
- report:2025-02-10-train-protocol
title: '[LYSWP2-6] Discrepancy between the actual locked and stored amount of tokens
  when using fee-on-transfer tokens'
vuln_class: []
---

# [LYSWP2-6] Discrepancy between the actual locked and stored amount of tokens when using fee-on-transfer tokens

_Section severity (from Solodit section header): Medium_  
_Audit firm: Hexens_  
_Source report: [2025-02-10-Train-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-10-Train-Protocol.md)_

---

**Severity:** Medium

**Path:** chains/evm/solidity/contracts/HashedTimeLockERC20.sol#L337-L350

**Description:** To bridge the funds the user needs to lock their funds on one chain to later unlock their funds on another chain. To do so the user can call the `lock()` function in the `HashedTimeLockERC20` contract:
```
if (token.balanceOf(msg.sender) < amount + reward) revert InsufficientBalance();
if (token.allowance(msg.sender, address(this)) < amount + reward) revert NoAllowance();

token.safeTransferFrom(msg.sender, address(this), amount + reward);
contracts[Id] = HTLC(
  amount,
  hashlock,
  uint256(1),
  tokenContract,
  timelock,
  uint8(1),
  payable(msg.sender),
  payable(srcReceiver)
);
```
However as the user given amount is being stored in the `contracts` mapping when using fee-on-transfer tokens the actual amount of tokens that will be transferred and locked in the contract will be less than the value stored in the mapping. This will lead to cases where when the user refunds or actually unlocks their tokens they will use the funds of other users.

If there is low amount of liquidity of that token it can lead to cases where the contract will be unable to refund or unlock the tokens because it will try to transfer the amount stored in the mapping while not having that amount of tokens actually on the contract.

**Remediation:**  Implement balance checks and store the balanceOf difference in the mapping instead of the user supplied amount.

**Status:**  Acknowledged

- - -
