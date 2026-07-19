---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-02-cyfrin-stakelink-vesting-v2-0-0-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-08-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-02-cyfrin-stakelink-vesting-v2-0
title: Missing access control in `SDLVesting::stakeReleasableTokens`
vuln_class: []
---

# Missing access control in `SDLVesting::stakeReleasableTokens`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-02-cyfrin-stakelink-vesting-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-02-cyfrin-stakelink-vesting-v2.0.md)_

---

**Description:** The [`SDLVesting::stakeReleasableTokens`](https://github.com/stakedotlink/contracts/blob/3462c0d04ff92a23843adf0be8ea969b91b9bf0c/contracts/vesting/SDLVesting.sol#L108) function is meant to be driven by a trusted staking bot, run by the Stake.Link team, to periodically take any newly-vested SDL and lock it into the SDLPool under the beneficiary’s chosen duration. However, it currently has no access control.

Thus anyone can call `SDLVesting::stakeReleasableTokens`. Using this an attacker can front run calls to `SDLVesting::release` by locking the beneficiaries tokens.

**Impact:** An adversary can repeatedly deny the beneficiary access to vested tokens by front running their `release()` transactions.

**Proof of Concept:**
```javascript
  it('should prevent griefing attacks', async () => {
      const { signers, accounts, start, vesting, sdlPool, sdlToken } = await loadFixture(deployFixture)

      await vesting.connect(signers[1]).setLockTime(4) // 4-year lock
      await time.increase(DAY)

      const releasableAmount = await vesting.releasable()
      console.log("Tokens victim wanted as liquid:", fromEther(releasableAmount), "SDL")

      await vesting.stakeReleasableTokens() //Someone frontruns and forces staking
      const lockIdAfter = await sdlPool.lastLockId()
      console.log("Frontrun with `stakeReleasableTokens`, position created with ID:", lockIdAfter.toString())
      console.log("Position owner:", await sdlPool.ownerOf(lockIdAfter), "(vesting contract)")

      // Get the staking position details
      const locks = await sdlPool.getLocks([lockIdAfter])
      const lock = locks[0]

      const currentTime = await time.latest()
      const lockDuration = Number(lock.duration)
      const unlockInitiationTime = Number(lock.startTime) + lockDuration / 2
      const fullUnlockTime = Number(lock.startTime) + lockDuration

      console.log("Base SDL staked:", fromEther(lock.amount), "SDL")
      console.log("Boost received:", fromEther(lock.boostAmount), "SDL")
      console.log("Total effective staking power:", fromEther(lock.amount + lock.boostAmount), "SDL")
      console.log("Lock duration:", lockDuration / (365 * 86400), "years")

      console.log("Years until unlock initiation allowed:", (unlockInitiationTime - currentTime) / (365 * 86400))
      console.log("Years until full withdrawal possible:", (fullUnlockTime - currentTime) / (365 * 86400))

      // Victim has almost no liquid tokens
      await vesting.connect(signers[1]).release() // Get the tiny remainder
      const victimLiquidBalance = await sdlToken.balanceOf(accounts[1])
      console.log("Victim's liquid balance:", fromEther(victimLiquidBalance), "SDL (instead of", fromEther(releasableAmount), "SDL)")

      // Victim transfers position to themselves, but it's still locked
      console.log("Transferring position to beneficiary...")
      await vesting.connect(signers[1]).withdrawRESDLPositions([4])
      console.log("Position now owned by:", await sdlPool.ownerOf(lockIdAfter))

      try {
        await sdlPool.connect(signers[1]).initiateUnlock(lockIdAfter)
        console.log("UNEXPECTED: Immediate unlock initiation succeeded!")
      } catch (error) {
        console.log("EXPECTED: Beneficiary cannot initiate unlock yet")
        console.log("Must wait 2 years before unlock can even be INITIATED, and another 2 years for full withdrawal")
      }
    })
```


**Recommended Mitigation:**
1. Introduce a `stakingBot` address that is the only non-beneficiary permitted to call the staking function:

   ```diff
   +    /// @notice Address of the trusted bot allowed to call stakeReleasableTokens
   +    address public stakingBot;
   ```

2. Set it in the constructor alongside `_owner` and `_beneficiary`:

   ```diff
       constructor(
           address _sdlToken,
           address _sdlPool,
           address _owner,
           address _beneficiary,
   +       address _stakingBot,
           uint64 _start,
           uint64 _duration,
           uint64 _lockTime
       ) {
           _transferOwnership(_owner);
   +       stakingBot = _stakingBot;
           …
       }
   ```

3. Create a combined access-control modifier allowing only the beneficiary *or* the staking bot:

   ```diff
   +    modifier onlyBeneficiaryOrBot() {
   +        if (msg.sender != beneficiary && msg.sender != stakingBot) {
   +            revert SenderNotAuthorized();
   +        }
   +        _;
   +    }
   ```

4. Apply that modifier to `stakeReleasableTokens()`:

   ```diff
   -    function stakeReleasableTokens() external {
   +    function stakeReleasableTokens() external onlyBeneficiaryOrBot {
           uint256 amount = releasable();
           if (amount == 0) revert NoTokensReleasable();
           …
       }
   ```

5. In case the bot’s key rotates or the Stake.Link team needs to change the automation address, add an owner-only setter:

   ```diff
   +    /// @notice Update the trusted staking bot address
   +    function setStakingBot(address _stakingBot) external onlyOwner {
   +        require(_stakingBot != address(0), "Invalid bot address");
   +        stakingBot = _stakingBot;
   +    }
   ```

With these changes, only the designated bot (and the beneficiary themselves, if desired) can trigger the periodic staking—eliminating the griefing vector that could otherwise lock tokens indefinitely.

**Stake.Link:** Fixed in commit [`565b043`](https://github.com/stakedotlink/contracts/commit/565b043b98f6b0a61a9eda9b7f2ca20ecdac8598)

**Cyfrin:** Verified. An address `staker` is now passed to the constructor. And a modifier `onlyBeneficiaryOrStaker` is applied to `stakeReleasableTokens`.

\clearpage
