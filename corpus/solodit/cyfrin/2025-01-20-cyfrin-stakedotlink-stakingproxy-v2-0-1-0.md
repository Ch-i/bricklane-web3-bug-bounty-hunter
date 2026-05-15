---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-01-20T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md
tags:
- firm:cyfrin
- report:2025-01-20-cyfrin-stakedotlink-stakingproxy-v2-0
title: Unrestricted reSDL token deposits with privileged withdrawals can lead to accidental
  loss of reSDL tokens
vuln_class: []
---

# Unrestricted reSDL token deposits with privileged withdrawals can lead to accidental loss of reSDL tokens

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-01-20-cyfrin-stakedotlink-stakingproxy-v2.0.md)_

---

**Description:** The `StakingProxy` contract implements ERC721 receiver functionality allowing it to receive reSDL tokens (ERC721) from any address. However, only the contract owner has the ability to withdraw these tokens.

This creates a risk where user owned reSDL tokens can get stuck if sent to the proxy accidentally or without understanding the withdrawal restrictions.

`StakingProxy.sol`

```solidity

// ----> @audit Anyone can transfer reSDL tokens to the proxy
function onERC721Received(address, address, uint256, bytes calldata) external returns (bytes4) {
    return this.onERC721Received.selector;
}

// ----> @audit Only owner can withdraw reSDL tokens
function withdrawRESDLToken(uint256 _tokenId, address _receiver) external onlyOwner {
    if (sdlPool.ownerOf(_tokenId) != address(this)) revert InvalidTokenId();
    IERC721(address(sdlPool)).safeTransferFrom(address(this), _receiver, _tokenId);
}
```
The reSDL tokens represent time-locked SDL staking positions that earn rewards. While the proxy's ability to hold reSDL tokens is an intended functionality for reward earning purposes, the unrestricted acceptance of transfers combined with privileged withdrawals creates unnecessary risk.

**Impact:** Any user accidentally transferring their reSDL tokens to the proxy has no direct way of recovering them without manual intervention of protocol team.


**Recommended Mitigation:** Consider gating the `onERC721Received` function to only accept transfers from authorized addresses that can be configured in the StakingProxy contract.

**Stake.link:**
Acknowledged.

**Cyfrin:** Acknowledged.
