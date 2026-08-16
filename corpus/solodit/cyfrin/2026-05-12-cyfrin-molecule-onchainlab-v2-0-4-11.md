---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-11
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: OnChainLabs lacks a dedicated wrapper for `EntryPoint::withdrawTo`, forcing
  owners through generic `execute`
vuln_class: []
---

# OnChainLabs lacks a dedicated wrapper for `EntryPoint::withdrawTo`, forcing owners through generic `execute`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** `OnChainLabs` is designed as an EIP-4337 Account Abstraction wallet. The wallet includes functions to receive and withdraw funds. Since it is an ERC-4337 wallet, it must deposit funds into the EntryPoint to cover transaction fees during normal operation.

The EntryPoint's deposit functionality is permissionless — anyone can deposit on behalf of any address. In practice, the wallet deposits funds on its own behalf to pay for user operation fees. However, funds stored in the EntryPoint deposit are only withdrawable by the depositing address itself, by calling `EntryPoint::withdrawTo`. This function is not implemented in the `OnChainLabs` wallet, making it impossible for the wallet to ever reclaim its deposited funds.

> ENTRY_POINT::StakeManager#withdrawTo
```solidity
    function withdrawTo(
        address payable withdrawAddress,
        uint256 withdrawAmount
    ) external virtual {
>>      DepositInfo storage info = deposits[msg.sender];
        uint256 currentDeposit = info.deposit;
        require(withdrawAmount <= currentDeposit, InsufficientDeposit(currentDeposit, withdrawAmount));
        info.deposit = currentDeposit - withdrawAmount;
        emit Withdrawn(msg.sender, withdrawAddress, withdrawAmount);
        (bool success, bytes memory ret) = withdrawAddress.call{value: withdrawAmount}("");
        require(success, DepositWithdrawalFailed(msg.sender, withdrawAddress, withdrawAmount, ret));
    }
```

Since `withdrawTo` uses `msg.sender` to identify the depositor, only the wallet contract itself can withdraw its own EntryPoint deposit. Without a corresponding function in the `OnChainLabs` wallet that forwards this call to the EntryPoint, any funds deposited there are inaccessible.

The only way to access these funds will be by constructing an operation to withdraw them, which is not a common thing in case of shutting down the wallet, where all funds should be able to be revoked directly.

**Impact:**
- All funds deposited by the wallet into the EntryPoint are permanently locked with no withdrawal path. If the wallet owner wishes to shut down the wallet and recover all funds, they can withdraw the balance held directly in the contract via `OnChainLabs::withdraw`, but any amount stored in the EntryPoint deposit will be irretrievably lost.

**Proof of Concept:**
1. A given wallet exists with `10 ETH` held in the contract and `1 ETH` deposited in the EntryPoint.
2. The wallet owner decides to shut down the wallet and withdraw all funds.
3. The owner calls `OnChainLabs::withdraw` to successfully recover the `10 ETH` held in the contract.
4. The `1 ETH` stored in the EntryPoint cannot be withdrawn, as the wallet has no function to call `EntryPoint::withdrawTo` on its own behalf, leaving the funds locked.

**Recommended Mitigation:** The `OnChainLabs` wallet should implement a function that allows the owner to withdraw funds stored in the EntryPoint by forwarding a call to `EntryPoint::withdrawTo`. Additionally, a corresponding deposit function should be implemented to allow the wallet to top up its EntryPoint balance in a controlled and explicit manner.

```solidity
function withdrawFromEntryPoint(
    address payable withdrawAddress,
    uint256 withdrawAmount
) external onlyEntryPointOrOwner {
    entryPoint().withdrawTo(withdrawAddress, withdrawAmount);
}

function depositToEntryPoint() external payable onlyEntryPointOrOwner {
    entryPoint().depositTo{value: msg.value}(address(this));
}
```

**Molecule:** Fixed in [8ee18b0](https://github.com/moleculeprotocol/onchainlabs/commit/8ee18b0).

**Cyfrin:** Verified.
