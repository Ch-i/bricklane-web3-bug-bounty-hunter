---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAO creator can inflate their privileges to mint/burn membership tokens, steal
  profits, and abuse approvals to `MembershipERC1155`
vuln_class: []
---

# DAO creator can inflate their privileges to mint/burn membership tokens, steal profits, and abuse approvals to `MembershipERC1155`

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** During the [creation of a new DAO](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L66-L70), the `MembershipFactory` contract is [granted](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L49) the `OWP_FACTORY_ROLE` which has special privileges to [mint](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L52-L59)/[burn](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L61-L67) tokens and execute any arbitrary call via [`MembershipERC1155::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L202-L210). Additionally, the calling account is [granted](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L48) the `DEFAULT_ADMIN_ROLE`; however, as [documented](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/49c0e4370d0cc50ea6090709e3835a3091e33ee2/contracts/access/AccessControl.sol#L40-L48), this bestows the power to manage all other roles as well.

This means that the creator of a given DAO can grant themselves the `OWP_FACTORY_ROLE` by calling `AccessControl::grantRole` and has a number of implications:
- Profit tokens can be stolen from callers of [`MembershipERC1155:sendProfit`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L189-L200), either by front-running and/or abusing dangling approvals.
- The DAO creator has unilateral control of the DAO and its membership tokens, so can mint/burn to/from any address.
- Profit can be stolen from the DAO by front-running a call to `MembershipERC1155::sendProfit` with a call to [`MembershipERC1155::burnBatchMultiple`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L85-L99) to ensure that [this conditional block](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L198-L200) is executed by causing the total supply of membership tokens to become zero. Alternatively, they can wait for the call to be executed and transfer the tokens directly using the arbitrary external call.

```solidity
if (_totalSupply > 0) {
    totalProfit[currency] += (amount * ACCURACY) / _totalSupply;
    IERC20(currency).safeTransferFrom(msg.sender, address(this), amount);
    emit Profit(amount);
} else {
    IERC20(currency).safeTransferFrom(msg.sender, creator, amount); // Redirect profit to creator if no supply
}
```

It is also prescient to note that this issue exists in isolation as a centralization risk of the One World Project owner itself, as detailed in a separate finding, who controls the `MembershipFactory` contract and thus all DAOs via [`MembershipFactory::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L155-L163).

**Impact:** The creator of a DAO can escalate their privileges to have unilateral control and steal profits from its members, as well as abusing any profit token approvals to the contract. All of the above is also possible for the One World Project owner, who has control of the factory and thus all DAOs created by it.

**Proof of Concept:** The following test can be added to `describe("ERC1155 and AccessControl Interface Support")` in `MembershipERC1155.test.ts`:
```javascript
it("can give OWP_FACTORY_ROLE to an address and abuse priviliges", async function () {
    const [factory, creator, user] = await ethers.getSigners();
    const membership = await MembershipERC1155.connect(factory).deploy();
    await membership.deployed();
    await membership.initialize("TestToken", "TST", tokenURI, creator.address);

    await membership.connect(creator).grantRole(await membership.OWP_FACTORY_ROLE(), creator.address);
    expect(await membership.hasRole(await membership.OWP_FACTORY_ROLE(), creator.address)).to.be.true;

    // creator can mint and burn at will
    await membership.connect(creator).mint(user.address, 1, 100);
    await membership.connect(creator).burn(user.address, 1, 50);

    await testERC20.mint(user.address, ethers.utils.parseEther("1"));
    await testERC20.connect(user).approve(membership.address, ethers.utils.parseEther("1"));

    const creatorBalanceBefore = await testERC20.balanceOf(creator.address);

    // creator can abuse approvals
    const data = testERC20.interface.encodeFunctionData("transferFrom", [user.address, creator.address, ethers.utils.parseEther("1")]);
    await membership.connect(creator).callExternalContract(testERC20.address, data);

    const creatorBalanceAfter = await testERC20.balanceOf(creator.address);
    expect(creatorBalanceAfter.sub(creatorBalanceBefore)).to.equal(ethers.utils.parseEther("1"));
});
```

**Recommended Mitigation:** Implement more fine-grained access controls for the DAO creator instead of granting the `DEFAULT_ADMIN_ROLE`.

**One World Project:** Given a separate role to the creator in [`a6b9d82`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/a6b9d82796c2d87a3924e8e80c3732474bf22506).

**Cyfrin:** Verified. `creator` now has a separate role `DAO_CREATOR ` that can only change URI.
