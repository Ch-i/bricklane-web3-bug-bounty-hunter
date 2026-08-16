---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-1-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Anyone can dodge reveal delays by providing unrelated account
vuln_class: []
---

# Anyone can dodge reveal delays by providing unrelated account

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `RLN` provides a commit-reveal functionality to slashing. Firstly, a commit happens:
```solidity
function slashCommit(address account, bytes32 hash) external onlyRole(SLASHER_ROLE) {
    uint256 lastReveal = lastRevealStartTime[account];
    uint256 revealStartTime;

    if (lastReveal == 0 || lastReveal + slashRevealWindowTime < block.timestamp) {
        revealStartTime = block.timestamp;
    } else {
        revealStartTime = lastReveal + slashRevealWindowTime;
    }

    slashCommitments[account][hash] = revealStartTime;
    lastRevealStartTime[account] = revealStartTime;
}
```
The hash is based on the private key of the private key and reward recipient address. Thus, a slasher might provide `(bob, hash(PK, slasherAddress))` as the inputs. Then, as he is the first to commit, that would store the earliest reveal start time and would be able to commit first:
```solidity
function slashReveal(
    address account,
    bytes32 privateKey,
    address rewardRecipient
)
    external
    onlyRole(SLASHER_ROLE)
{
    /// forge-lint: disable-next-line(asm-keccak256)
    bytes32 hash = keccak256(abi.encodePacked(privateKey, rewardRecipient));
    uint256 revealStartTime = slashCommitments[account][hash];

    if (revealStartTime == 0) {
        revert RLN__InvalidCommitment();
    }

    if (block.timestamp < revealStartTime) {
        revert RLN__RevealWindowNotStarted();
    }

    delete slashCommitments[account][hash];
    slash(privateKey, rewardRecipient);
}
```

The issue is that the `account` provided actually serves no real purpose. Another slasher can simply provide `(randomAddress, hash(PK, otherSlasherAddress))`. This will get a 0 delay as this account has not been used, thus the reveal will be possible immediately. `slashCommitments` would be based on the `randomAddress, hash` keys, then during the reveal, he simply has to provide `(randomAddress, PK, otherSlasherAddress)` and the account is only used for accessing and deleting that same `slashCommitments` mapping. Thus, it is not enforced at all that the account actually corresponds to the slashed address.

**Impact:** Any slasher can get the rewards for himself as he is dodging the delay completely.

**Recommended Mitigation:** Enforce the account provided to actually be the slashed account. The easiest way is to do it upon the reveal when the PK is known and validate it against the user in `members[poseidonHash(privateKey)]`.

**StatusL2:** Fixed in [62021fc](https://github.com/status-im/status-network-monorepo/commit/62021fce4df10101598e02004049d7a14e7f2d00).

**Cyfrin:** Verified.
