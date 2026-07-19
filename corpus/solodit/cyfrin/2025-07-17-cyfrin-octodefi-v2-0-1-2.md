---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Automation DoS via blacklisted or reverting fee recipients
vuln_class: []
---

# Automation DoS via blacklisted or reverting fee recipients

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `FeeHandler.handleFee()` uses `safeTransferFrom()` to forward ERC-20 tokens to `beneficiary`, `creator`, `vault`, and `burnerAddress`. If any of those addresses are **black-listed** by USDT/USDC (transfer returns false) the call reverts.
`handleFeeETH()` uses `transfer()` which has a limitation of 2300 gas units; if the destination contract’s `receive()` reverts, for example a smart contract wallet that executes more logic than could be covered by the gas limit, the whole automation fails.
```solidity
IERC20(token).safeTransferFrom(msg.sender, beneficiary, beneficiaryAmount);

if (creator != address(0)) {
    IERC20(token).safeTransferFrom(msg.sender, creator, creatorAmount);
    IERC20(token).safeTransferFrom(msg.sender, vault, vaultAmount);
} else {
    IERC20(token).safeTransferFrom(msg.sender, vault, vaultAmount + creatorAmount);
}

if (burnAmount > 0) {
    IERC20(token).safeTransferFrom(msg.sender, burnerAddress, burnAmount);
}
```

```solidity
payable(beneficiary).transfer(beneficiaryAmount);

if (creator != address(0)) {
    payable(creator).transfer(creatorAmount);
    payable(vault).transfer(vaultAmount);
} else {
    payable(vault).transfer(vaultAmount + creatorAmount);
}

if (burnAmount > 0) {
    payable(burnerAddress).transfer(burnAmount);
}
```
**Impact:** Denial of service on all future `executeAutomation()` calls for the strategies with a blacklisted or reverting `creator`.

**Recommended Mitigation:** Use a **pull** pattern where each entity could claim fees on its own instead of a push funds model, or `try/catch` around transfers so a single failing destination cannot block execution. Additionally avoid making native token transfers using `transfer()` but rather leverage some library that implements safe native token transfers.

**OctoDeFi:** Fixed in PR [\#14](https://github.com/octodefi/strategy-builder-plugin/pull/14).

**Cyfrin:** Verified. A withdrawal method has been implemented to allow users to claim their accumulated fee balances. Note that native token transfers still rely on the `transfer()` method which should also be updated. Application of the `nonReentrant()` modifier is also not necessary.

**OctoDeFi:** Fixed in commit [7c48784](https://github.com/octodefi/strategy-builder-plugin/commit/7c48784640163998a9265f580d3b18aa46bc36a6).

**Cyfrin:** Verified. The Solady `SafeTransferLib` is now used for all token transfers.
