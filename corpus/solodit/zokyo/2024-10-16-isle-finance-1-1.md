---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Incorrect Shares Attributed While Depositing
vuln_class: []
---

# Incorrect Shares Attributed While Depositing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity** - Informational

**Status** - Acknowledged

**Description**: 

When depositing the Pool contract follows the ERC4626 standard as follows →
```solidity
 function deposit(uint256 assets, address receiver) public override returns (uint256 shares) {
        // Checks: receiver is not the zero address.
        if (receiver == address(0)) revert Errors.Pool_RecipientZeroAddress();


        // Checks: deposit amount is less than or equal to the max deposit.
        if (assets > maxDeposit(receiver)) revert Errors.Pool_DepositGreaterThanMax(assets, maxDeposit(receiver));


        shares = previewDeposit(assets);
        _deposit(_msgSender(), receiver, assets, shares);


        return shares;
    }
```
The shares minted are calculated via the previewDeposit function(which uses _convertToShares()) in the ERC4626 library , but in the isle ecosystem this would be incorrect and more than required shares would be minted to the user . This is because this calculation does not include the unrealized losses in the system . To correctly account for the unrealized losses , instead of using previewDeposit , use  _convertToExitShares() .

The same is applicable for the minting function where _convertToExitShares should be used instead.

**Recommendation**:

Use the recommended functions instead.

**Client comment**: We use unrealizedLoss to create a less favorable exchange rate, hoping to discourage users from withdrawing in the event of a loan impairment. This approach serves as a soft deterrent rather than a direct prevention of withdrawals. The unrealizedLoss itself only affects withdrawals and does not impact deposits.
