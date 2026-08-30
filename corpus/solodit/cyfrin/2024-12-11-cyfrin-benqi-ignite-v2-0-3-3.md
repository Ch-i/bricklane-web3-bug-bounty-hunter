---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Unnecessary `amount` parameter in `StakingContract::stakeWithERC20`
vuln_class: []
---

# Unnecessary `amount` parameter in `StakingContract::stakeWithERC20`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** When provisioning a node through [`StakingContract::stakeWithERC20`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L513-L577), users can pay with a supported ERC20 token. The [`totalRequiredToken`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L527-530) is calculated based on the [`avaxStakeAmount`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L35) (needed to register the node in Ignite) and the [`hostingFee`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L525) (paid to Zeeve for hosting), before being [transferred](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L534-539) from the user to the contract:

```solidity
require(isTokenAccepted(token), "Token not accepted");
uint256 hostingFee = calculateHostingFee(duration);

uint256 totalRequiredToken = convertAvaxToToken(
    token,
    avaxStakeAmount + hostingFee
);

require(amount >= totalRequiredToken, "Insufficient token");

// Transfer tokens from the user to the contract
IERC20Upgradeable(token).safeTransferFrom(
    msg.sender,
    address(this),
    totalRequiredToken
);
```

The [`amount`](https://code.zeeve.net/zeeve-endeavors/benqi_smartcontract/-/blob/b63336201f50f9a67451bf5c7b32ddcc4a847ce2/contracts/staking.sol#L521) parameter provided by the user is only used to validate that it covers the `totalRequiredToken`, but since execution will revert if the user has not given the contract sufficient allowance for the transfer, the `amount` parameter becomes redundant.

**Recommended Mitigation:** Consider removing the `amount` parameter from `StakingContract::stakeWithERC20`.

**BENQI:** Acknowledged. The purpose is to ensure that the value passed in by the frontend is not lower than the `totalRequiredToken`, acting as a form of slippage check. If it’s lesser than totalRequiredToken, more tokens could be deducted than the user expected.

**Cyfrin:** Acknowledged.
