---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-06-17-cyfrin-templedao-v2-1-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-06-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md
tags:
- firm:cyfrin
- report:2024-06-17-cyfrin-templedao-v2-1
title: Malicious users can double their voting power.
vuln_class: []
---

# Malicious users can double their voting power.

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-06-17-cyfrin-templedao-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-06-17-cyfrin-templedao-v2.1.md)_

---

**Description:** When calculating The `voteWeight` of a delegatee, its own `ownVoteWeight` is added. This makes it possible for some users to double their voting power by constructing a cycle. For example, Alice delegates Bob, Bob delegates Alice.

```solidity

    function getDelegatedVoteWeight(address _delegate) external view returns (uint256) {
        // check address is delegate
        uint256 ownVoteWeight = _voteWeight(_delegate, _balances[_delegate]);
        address callerDelegate = userDelegates[_delegate];
        if (!delegates[_delegate] || callerDelegate == msg.sender) { return ownVoteWeight; }
@>      return ownVoteWeight + _voteWeight(_delegate, _delegateBalances[_delegate]);
    }
```

**Impact:** Malicious users can double their voting power.

**Proof of Concept:** Here's an example scenario:
    1. Alice delegated his voting weight 100 to Bob.
    2. Bob delegated his voting weight 200 to Alice.
    3. The total sum of _delegateBalances of Alice and Bob is (100 + 200) + (200 + 100) = 600.

**Recommended Mitigation:** There might be several ways to mitigate the issue, here's a few:

-The first way

Delegating itself should not be allowed.

```diff

-   function unsetUserVoteDelegate() external override {
+   function unsetUserVoteDelegate() public override {

    function setSelfAsDelegate(bool _approve) external override {
            [...]
+       if (_approve && !prevStatusTrue) unsetUserVoteDelegate();
    }
```

And, any delegatee should not be allowed to delegate.

```diff

    function setUserVoteDelegate(address _delegate) external override {
        if (_delegate == address(0)) { revert CommonEventsAndErrors.InvalidAddress(); }
        if (!delegates[_delegate]) {  revert InvalidDelegate(); }
+       if (userDelegates[msg.sender] == msg.sender) { revert(); }
            [...]
    }

```

-The second way

`ownVoteWeight` should not be add, unless if a user delegate himself. This is the typical way for calculationg woting power.

```diff

    function getDelegatedVoteWeight(address _delegate) external view returns (uint256) {
        // check address is delegate
-       uint256 ownVoteWeight = _voteWeight(_delegate, _balances[_delegate]);
-       address callerDelegate = userDelegates[_delegate];
-       if (!delegates[_delegate] || callerDelegate == msg.sender) { return ownVoteWeight; }
-       return ownVoteWeight + _voteWeight(_delegate, _delegateBalances[_delegate]);
        return _voteWeight(_delegate, _delegateBalances[_delegate]);
    }

```

**TempleDAO:** Fixed in [PR 1040](https://github.com/TempleDAO/temple/pull/1040)

**Cyfrin:** Verified
