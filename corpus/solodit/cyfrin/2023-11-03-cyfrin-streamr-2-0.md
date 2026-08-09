---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-03-cyfrin-streamr-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-03T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
tags:
- firm:cyfrin
- report:2023-11-03-cyfrin-streamr
title: Unsafe use of `transfer()/transferFrom()` with `IERC20`
vuln_class: []
---

# Unsafe use of `transfer()/transferFrom()` with `IERC20`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-03-cyfrin-streamr.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md)_

---

Some tokens do not implement the ERC20 standard properly but are still accepted by most code that accepts ERC20 tokens. For example Tether (USDT)'s `transfer()` and `transferFrom()` functions on L1 do not return booleans as the specification requires, and instead have no return value. Consider using OpenZeppelin’s `SafeERC20`'s `safeTransfer()/safeTransferFrom()` instead

```solidity
File: contracts\OperatorTokenomics\Operator.sol
264:         token.transferFrom(_msgSender(), address(this), amountWei);
442:         token.transfer(msgSender, rewardDataWei);

File: contracts\OperatorTokenomics\Sponsorship.sol
187:         token.transferFrom(_msgSender(), address(this), amountWei);
215:         token.transferFrom(_msgSender(), address(this), amountWei);
261:         token.transfer(streamrConfig.protocolFeeBeneficiary(), slashedWei);
273:         token.transfer(operator, payoutWei);

File: contracts\OperatorTokenomics\OperatorPolicies\QueueModule.sol
86:           token.transfer(delegator, amountDataWei);

File: contracts\OperatorTokenomics\OperatorPolicies\StakeModule.sol
128:         token.transfer(streamrConfig.protocolFeeBeneficiary(), protocolFee);
```

**Client:** We will only use DATA token in our system. It doesn't have the above methods. So: `transfer` it is.

**Cyfrin:** Acknowledged.
