---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-06-06-sign-staking-3-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-06-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md
tags:
- firm:codespect
- report:2025-06-06-sign-staking
title: '[I-01] NFT contract has features which can influence unstaking'
vuln_class: []
---

# [I-01] NFT contract has features which can influence unstaking

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-06-06-SIGN-Staking.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-06-06-SIGN-Staking.md)_

---

**Files:** [SIGNStaking.sol](https://github.com/EthSign/sign-token-staking-evm/blob/735cc008ea45c4a54e87761217218fb3983e69d5/src/SIGNStaking.sol)

**Description:**

The SIGN staking contract allows users to stake a SIGN NFT to boost their APR. The implementation of the NFT contract can be found [here](https://etherscan.deth.net/address/0x20a05ad37d350c800463d531d248c953537da297#code). This NFT contract includes two functions that may interfere with the unstaking process:

```solidity
function burn(uint256[] calldata ids) external onlyOwner {
    for (uint256 i = 0; i < ids.length; i++) {
        _burn(ids[i]);
    }
}

function freeze(uint256[] calldata ids) external onlyOwner {
    for (uint256 i = 0; i < ids.length; i++) {
        _getSignNFTStorage().frozenIds[ids[i]] = true;
    }
}
```

The `burn(...)` function permanently removes the NFT, while `freeze(...)` prevents it from being transferred. If either of these actions is performed on an NFT currently staked in the SIGNStaking contract, the user will be unable to withdraw their stake. This is because the following line in the `unstake(...)` function will revert:

```solidity
if (userStake.nftStakeTime > 0) {
    $.nftContract.safeTransferFrom(address(this), msg.sender, userStake.nftTokenId);
}
```

Additionally, users may still be accumulating boosted interest despite the NFT being frozen or burned, which is likely unintended behaviour.

**Impact:** A user’s stake can become permanently locked if the associated NFT is frozen or burned. While this is primarily a centralisation risk (since Sign controls both contracts), it could still impact user trust and usability.

**Recommendation:**

- Allow users to unstake their SIGN tokens even if the associated NFT is no longer transferable.
- Stop boosted interest accrual for NFTs that are frozen or burned.

**Status:** Acknowledged

**Update from TokenTable:** Acknowledged
