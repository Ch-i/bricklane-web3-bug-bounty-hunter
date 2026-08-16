---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Multiple L2 `BridgeToken` can be associated with the same L1 `NativeToken`
  by using `TokenBridge::setCustomContract`
vuln_class: []
---

# Multiple L2 `BridgeToken` can be associated with the same L1 `NativeToken` by using `TokenBridge::setCustomContract`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** Multiple L2 `BridgeToken` can be associated with the same L1 `NativeToken` by using `TokenBridge::setCustomContract`.

This was not introduced in the latest changes but is present in the current mainnet `TokenBridge` [code](https://github.com/Consensys/linea-contracts/blob/main/contracts/tokenBridge/TokenBridge.sol).

**Impact:** This breaks the `TokenBridge` invariant that one L1 `NativeToken` should only be associated with one L2 `BridgeToken`.

**Proof of Concept:** Add this PoC to `test/tokenBridge/E2E.ts` under the `setCustomsContract` section:
```typescript
    it("Multiple L2 BridgeTokens can be associated with a single L1 NativeToken by using setCustomContract", async function () {
      const {
        user,
        l1TokenBridge,
        l2TokenBridge,
        tokens: { L1USDT },
      } = await loadFixture(deployContractsFixture);

      // @audit the setup of this PoC has been copied from the test
      // "Should mint and burn correctly from a target contract"
      const amountBridged = 100;

      // Deploy custom contract
      const CustomContract = await ethers.getContractFactory("MockERC20MintBurn");
      const customContract = await CustomContract.deploy("CustomContract", "CC");

      // Set custom contract
      await l2TokenBridge.setCustomContract(await L1USDT.getAddress(), await customContract.getAddress());

      // @audit save user balance before both bridging attempts
      const USDTBalanceBefore = await L1USDT.balanceOf(user.address);

      // Bridge token (allowance has been set in the fixture)
      await l1TokenBridge.connect(user).bridgeToken(await L1USDT.getAddress(), amountBridged, user.address);

      expect(await L1USDT.balanceOf(await l1TokenBridge.getAddress())).to.be.equal(amountBridged);
      expect(await customContract.balanceOf(user.address)).to.be.equal(amountBridged);
      expect(await customContract.totalSupply()).to.be.equal(amountBridged);

      // @audit deploy a new second custom contract
      const customContract2 = await CustomContract.deploy("CustomContract2", "CC2");

      // @audit using setCustomContract, this second L2 BridgeToken can be associated
      // with L1USDT Token even though it should be impossible to do this as L1USDT has
      // already been bridged and already has a paired L2 BridgeToken
      //
      // @audit Once the suggested fix is applied, this should revert
      await l2TokenBridge.setCustomContract(await L1USDT.getAddress(), await customContract2.getAddress());

      // @audit same user now bridges L1->L2 again
      await l1TokenBridge.connect(user).bridgeToken(await L1USDT.getAddress(), amountBridged, user.address);

      // @audit L1 TokenBridge has twice the balance
      expect(await L1USDT.balanceOf(await l1TokenBridge.getAddress())).to.be.equal(amountBridged*2);

      // @audit first L2 BridgeToken still has the same balance and supply
      expect(await customContract.balanceOf(user.address)).to.be.equal(amountBridged);
      expect(await customContract.totalSupply()).to.be.equal(amountBridged);

      // @audit second L2 BridgeToken received new balance and supply from second bridging
      expect(await customContract2.balanceOf(user.address)).to.be.equal(amountBridged);
      expect(await customContract2.totalSupply()).to.be.equal(amountBridged);

      // @audit user L1 USDT balance deducted due to both bridging attempts
      const USDTBalanceAfterTwoL1ToL2Bridges = await L1USDT.balanceOf(user.address);
      expect(USDTBalanceBefore - USDTBalanceAfterTwoL1ToL2Bridges).to.be.equal(amountBridged*2);

      // @audit user now bridges back from first L2 BridgeToken
      await l2TokenBridge.connect(user).bridgeToken(await customContract.getAddress(), amountBridged, user.address);

      // @audit first L2 BridgeToken has 0 balance and supply
      expect(await customContract.balanceOf(user.address)).to.be.equal(0);
      expect(await customContract.totalSupply()).to.be.equal(0);

      // @audit user then bridges back from second L2 BridgeToken
      await l2TokenBridge.connect(user).bridgeToken(await customContract2.getAddress(), amountBridged, user.address);

      // @audit second L2 BridgeToken has 0 balance and supply
      expect(await customContract2.balanceOf(user.address)).to.be.equal(0);
      expect(await customContract2.totalSupply()).to.be.equal(0);

      // @audit user should have received back both bridged amounts
      const USDTBalanceAfter = await L1USDT.balanceOf(user.address);
      expect(USDTBalanceAfter - USDTBalanceAfterTwoL1ToL2Bridges).to.be.equal(amountBridged*2);

      // @audit user ends up with initial token amount
      expect(USDTBalanceAfter).to.be.equal(USDTBalanceBefore);

      // @audit user was able to bridge L1->L2 to two different L2 BridgeTokens,
      // and was able to bridge back L2->L1 from both different L2 BridgeTokens back
      // into the same L1 NativeToken. This breaks the invariant that one L1 NativeToken
      // should only be associated with one L2 BridgeToken
    });
```

Run with: `npx hardhat test --grep "Multiple L2 BridgeTokens can be associated with"`

**Recommended Mitigation:** `TokenBridge::setCustomContract` should prevent multiple L2 `BridgeToken` from being associated with the same L1 `NativeToken`. One possible implementation is to add this check:
```solidity
  function setCustomContract(
    address _nativeToken,
    address _targetContract
  ) external nonZeroAddress(_nativeToken) nonZeroAddress(_targetContract) onlyOwner isNewToken(_nativeToken) {
    if (bridgedToNativeToken[_targetContract] != EMPTY) {
      revert AlreadyBrigedToNativeTokenSet(_targetContract);
    }
    if (_targetContract == NATIVE_STATUS || _targetContract == DEPLOYED_STATUS || _targetContract == RESERVED_STATUS) {
      revert StatusAddressNotAllowed(_targetContract);
    }

    // @audit proposed fix
    uint256 targetChainIdCache = targetChainId;

    if (nativeToBridgedToken[targetChainIdCache][_nativeToken] != EMPTY) {
      revert("Already set a custom contract for this native token");
    }

    nativeToBridgedToken[targetChainIdCache][_nativeToken] = _targetContract;
    bridgedToNativeToken[_targetContract] = _nativeToken;
    emit CustomContractSet(_nativeToken, _targetContract, msg.sender);
  }
```

**Linea:**
Fixed in commit [35c7807](https://github.com/Consensys/zkevm-monorepo/commit/35c7807756ccac2756be7da472f5e6ce0fd9b16a#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L388-R394) merged in [PR3249](https://github.com/Consensys/zkevm-monorepo/pull/3249/files#diff-e5dcf44cdbba69f5a1f8fc58700577ce57caac0c15a5d5fb63e0620aeced62d4L388-R397).

**Cyfrin:** Verified.
