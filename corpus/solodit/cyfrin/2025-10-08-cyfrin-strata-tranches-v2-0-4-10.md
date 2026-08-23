---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-10
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: '`UnstakeCooldown::balance` requires a different token contract than the actual
  token that is reporting the balance for'
vuln_class: []
---

# `UnstakeCooldown::balance` requires a different token contract than the actual token that is reporting the balance for

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The `UnstakeCooldown` contract is used when withdrawing `USDe`. It is meant to allow the system to request the cooldown of `sUSDe` on the Ethena contract and then `unstake` the underlying `USDe` to be sent to the user.
When a cooldown is requested on the `sUSDe` contract, the underlying amount of `USDe` that will be given to the user is tracked on `cooldown.underlyingAmount`.

So, `cooldowns` on `sUSDe` returns the amount of `USDe`, which means, querying `proxy.getPendingAmount()` returns amounts of `USDe`, not `sUSDe`.
- This means, `UnstakeCooldown::balanceOf` is querying amounts of `USDe` for the `user`, not `sUSDe`, but the request on the `activeRequests` mapping was associated with `sUSDe` instead of `USDe`. This forces the users to call `balanceOf()` specifying `sUSDe` as the token when in reality they are querying amounts of `USDe`.

```solidity
//sUSDeStrategy::withdraw//
    function withdraw (address tranche, address token, uint256 tokenAmount, uint256 baseAssets, address receiver) external onlyCDO returns (uint256) {
        ...
        if (token == address(USDe)) {
@>          unstakeCooldown.transfer(sUSDe, receiver, shares);
            return baseAssets;
        }
        revert UnsupportedToken(token);
    }

//UnstakeCooldown::transfer//
function transfer(IERC20 token, address to, uint256 amount) external {
    ...

@>  TRequest[] storage requests = activeRequests[address(token)][to];
    IUnstakeHandler[] storage proxies = proxiesPool[address(token)][to];

    ...

    requests.push(TRequest(uint64(unlockAt), proxy));
    emit Requested(address(token), to, amount, unlockAt);
}

function balanceOf (IERC20 token, address user, uint256 at) public view returns (uint256) {
@>  TRequest[] storage requests = activeRequests[address(token)][user];
    uint256 l = requests.length;
    uint256 balance = 0;
    for (uint256 i = 0; i < l; i++) {
        TRequest memory req = requests[i];
        if (req.unlockAt <= at) {
@>          balance += req.proxy.getPendingAmount();
        }
    }
    return balance;
}

//sUSDeCooldownRequestImpl//

    function getPendingAmount () external view returns (uint256 amount) {
@>      amount = sUSDe.cooldowns(address(this)).underlyingAmount;
        return amount;
    }

```


**Recommended Mitigation:** When registering a new request, associate it with `USDe` instead of `sUSDe`. The rest of the code would work fine, and the users would now input `USDe` as the token and get amounts of `USDe`. Additionally, it might be worth documenting that the reported balance corresponds to `USDe` units.

**Strata:**
Acknowledged; changing the accepted token in balanceOf to the underlying token could break the finalization logic, since the underlying token may later be used in different staked tokens. Here we want to stay focused on the specific staked asset.
