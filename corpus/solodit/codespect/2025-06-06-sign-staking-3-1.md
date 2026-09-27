---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-3-1
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[I-02] Checks effects interactions pattern not followed by several functions'
vuln_class: []
---

# [I-02] Checks effects interactions pattern not followed by several functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Original severity:** Best Practices

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol)

**Description:**

Several functions in the contract do not follow the Checks-Effects-Interactions (CEI) pattern. In these cases, state variables are updated *after* performing external interactions, which goes against best practices:

```solidity
function unstakeNFT() external nonReentrant {
    // ...
    $.nftContract.safeTransferFrom(address(this), msg.sender, tokenId);
    userStake.nftTokenId = 0;
    userStake.nftStakeTime = 0;
    // ...
}

function stakeNFT(uint256 tokenId) external nonReentrant whenConfigured whenNotPaused {
    // ...
    $.nftContract.transferFrom(msg.sender, address(this), tokenId);
    userStake.nftTokenId = tokenId;
    userStake.nftStakeTime = block.timestamp;
    // ...
}

function stake(uint256 amount) external nonReentrant whenConfigured whenNotPaused {
    // ...
    $.signToken.safeTransferFrom(msg.sender, address(this), amount);
    userStake.principalAmount += amount;
    // ...
}
```

*Note: Some of these external interactions do not pose a reentrancy risk, but it is still best practice to follow the CEI pattern.*

**Impact:** There is no danger of reentrancy as functions are protected by the `nonReentrant` modifier, however, it is a best practice to always follow the CEI pattern.

**Recommendation:** Reorder the statements in affected functions so that all state changes occur before any external interaction.

**Status:** Fixed

**Update from TokenTable:** [e14dcc9b159afb4699e80a3ce820380190fde774](https://github.com/EthSign/sign-token-staking-evm/commit/e14dcc9b159afb4699e80a3ce820380190fde774)
