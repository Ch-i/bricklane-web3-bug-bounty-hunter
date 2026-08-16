---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-H-1 Attacker can freeze profit withdrawals from V3 vaults
vuln_class: []
---

# TRST-H-1 Attacker can freeze profit withdrawals from V3 vaults

_Section severity (from Solodit section header): High_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
Users of Ninja can use Vault's `withdrawProfit()` to withdraw profits. It starts with the 
following check:
 
```solidity 
   if (block.timestamp <= lastProfitTime) {
      revert NYProfitTakingVault__ProfitTimeOutOfBounds();
      }

```
If attacker can front-run user's `withdrawProfit()` TX and set **lastProfitTime** to 
block.timestamp, they would effectively freeze the user's yield. That is indeed possible using 
the Vault paired strategy's `harvest()` function. It is permissionless and calls `_harvestCore()`. 
The attack path is shown in **bold**.

```solidity 
      function harvest() external override whenNotPaused returns (uint256 callerFee) {
            require(lastHarvestTimestamp != block.timestamp);
                uint256 harvestSeconds = lastHarvestTimestamp > 0 ? block.timestamp 
            - lastHarvestTimestamp : 0;
      lastHarvestTimestamp = block.timestamp;
                uint256 sentToVault;
          uint256 underlyingTokenCount;
     (callerFee, underlyingTokenCount, sentToVault) = _harvestCore();
            emit StrategyHarvest(msg.sender, underlyingTokenCount, 
                   harvestSeconds, sentToVault);
                }
```

```solidity
      function _harvestCore() internal override returns (uint256 callerFee, uint256 underlyingTokenCount,      uint256 sentToVault)
            {
        IMasterChef(SPOOKY_SWAP_FARM_V2).deposit(POOL_ID, 0);
            _swapFarmEmissionTokens();
                callerFee = _chargeFees();
                    underlyingTokenCount = balanceOf();
                       sentToVault = _sendYieldToVault();
            } 
```
```solidity
      function _sendYieldToVault() internal returns (uint256 sentToVault) {
         sentToVault = IERC20Upgradeable(USDC).balanceOf(address(this));
            if (sentToVault > 0) {
               IERC20Upgradeable(USDC).approve(vault, sentToVault);
            IVault(vault).depositProfitTokenForUsers(sentToVault);
                }
                  }
```
```solidity
      function depositProfitTokenForUsers(uint256 _amount) external nonReentrant {
         if (_amount == 0) {
            revert NYProfitTakingVault__ZeroAmount();
         }
        if (block.timestamp <= lastProfitTime) {
            revert NYProfitTakingVault__ProfitTimeOutOfBounds();
         }
        if (msg.sender != strategy) {
            revert NYProfitTakingVault__OnlyStrategy();
        }
            uint256 totalShares = totalSupply();
        if (totalShares == 0) {
            lastProfitTime = block.timestamp;
            return;
          }
            accProfitTokenPerShare += ((_amount * PROFIT_TOKEN_PER_SHARE_PRECISION) / totalShares);
               lastProfitTime = block.timestamp;
            // Now pull in the tokens (Should have permission)
            // We only want to pull the tokens with accounting
               profitToken.transferFrom(strategy, address(this), _amount);
            emit ProfitReceivedFromStrategy(_amount);
                }
```
**Recommended Mitigation:**
Do not prevent profit withdrawals during lastProfitTime block.

**Team response:**
Accepted and removed.
