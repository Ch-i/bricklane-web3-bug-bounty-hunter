---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Allowing anyone to finalize any withdrawal can lead to integration problems
  for smart contract allowed to receive ETH
vuln_class: []
---

# Allowing anyone to finalize any withdrawal can lead to integration problems for smart contract allowed to receive ETH

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** Current implementation of `swEXIT::finalizeWithdrawal` allows anyone to finalize any withdrawal request which is already processed. However this design decision make the strong assumption that an NFT owner always wants to finalize a withdrawal, which might not be always the case.

**Impact:** Allowing anyone to finalize any withdrawal request already processed can lead to stuck ETH in some smart contracts

**POC:**
Assume a protocol which goals is facilitating NFT auctions, with auctions that can accept any token or ETH. Bidders has a record for the amount of tokens/ETH they are offering for an NFT, so the smart contract implement a `receive` function to accept ETH.

Eve initiate a withdrawal request, but given that she urge for ETH she decide to use this protocol to sell her NFT in an auction. To do this, she must transfer the NFT to the auction contract.

Alice decide to bid for the NFT, and at the end of the auction she wins, now she has to claim the NFT (the auction contract is the owner of the NFT right now).

The swEXIT NFT is processed before Alice intend to claim it, Eve calls `finalizeWithdrawal` with the NFT in the auction contract, given that this contract is allowed to receive ETH and it is the NFT owner the transaction does not revert, and the ETH associated to the NFT now is stuck forever in the auction contract, Alice cannot claim nothing now.

**Recommended Mitigation:** Only allowed the owner of the NFT to finalize a withdrawal

```diff
    function finalizeWithdrawal(uint256 tokenId) external override {
        if (AccessControlManager.withdrawalsPaused()) {
        revert WithdrawalsPaused();
        }

        address owner = _ownerOf(tokenId);

-       if (owner == address(0)) {
-           revert WithdrawalRequestDoesNotExist();
+       if (owner == msg.sender) {
+           revert WithdrawalRequestFinalizationOnlyAllowedForNFTOwner();
        }
```

**Swell:** Fixed in commit [b5d7a19](https://github.com/SwellNetwork/v3-contracts-lst/commit/b5d7a19e2f6de5c0ae086c8deaac5166767cd3fd).

**Cyfrin:**
Verified.
