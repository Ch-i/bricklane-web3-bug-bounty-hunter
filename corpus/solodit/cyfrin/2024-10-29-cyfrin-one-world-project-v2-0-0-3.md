---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-0-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: One World Project has unilateral control over all DAOs, allowing the owner
  to update tier configurations, mint/burn membership tokens, steal profits, and abuse
  token approvals to `MembershipFactory` and `MembershipERC1155` proxy contracts
vuln_class: []
---

# One World Project has unilateral control over all DAOs, allowing the owner to update tier configurations, mint/burn membership tokens, steal profits, and abuse token approvals to `MembershipFactory` and `MembershipERC1155` proxy contracts

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When the `MembershipFactory` contract is deployed, the `EXTERNAL_CALLER` role is granted to the caller. This allows the One World Project to update the tiers configurations for a specific DAO via [`MembershipFactory::updateDAOMembership`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L90-L117) and execute any arbitrary call via [`MembershipFactory::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L155-L163). Additionally, during the [creation of a new DAO](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L66-L70), the `MembershipFactory` contract is [granted](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L49) the `OWP_FACTORY_ROLE` which has special privileges to [mint](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L52-L59)/[burn](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L61-L67) tokens and execute any arbitrary call via [`MembershipERC1155::callExternalContract`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/tokens/MembershipERC1155.sol#L202-L210).

While unilateral control over DAO tier configurations alone is prescient to note, the chaining of `MembershipFactory::callExternalContract` and `MembershipERC1155::callExternalContract` calls is incredibly dangerous without any restrictions on the target function selectors and contracts to be called. As a consequence, similar to the other privilege escalation vulnerability, the One World Project owner has the ability to arbitrarily mint/burn membership tokens for all DAOs, steal profits, and abuse approvals to `MembershipERC1155` proxy contracts. Furthermore, `MembershipFactory::callExternalContract` can be used to abuse approvals given to this contract directly, by front-running or otherwise – if a user sets the maximum `uint256` allowance on joining a DAO, the One World Project owner could drain their entire token balance for the given currency.

**Impact:** The One World Project owner has unilateral control of the `MembershipFactory` contract and thus all DAOs created by it, meaning profits can be stolen from its members and profit token approvals to the proxy contracts abused. The One World Project owner could also drain the balances of any tokens with dangling approvals to the `MembershipFactory` contract. This is especially problematic if the owner address becomes compromised in any way.

**Proof of Concept:** The following test can be added to `describe("Call External Contract")` in `MembershipFactory.test.ts`:
```javascript
it("allows admin to have unilateral power", async function() {
  await testERC20.mint(addr1.address, ethers.utils.parseEther("2"));
  await testERC20.connect(addr1).approve(membershipFactory.address, ethers.utils.parseEther("1"));

  await currencyManager.addCurrency(testERC20.address);  // Assume addCurrency function exists in CurrencyManager
  const tx = await membershipFactory.createNewDAOMembership(DAOConfig, TierConfig);
  const receipt = await tx.wait();
  const event = receipt.events.find((event:any) => event.event === "MembershipDAONFTCreated");
  const nftAddress = event.args[1];
  const membershipERC1155 = await MembershipERC1155.attach(nftAddress);

  let ownerBalanceBefore = await testERC20.balanceOf(owner.address);

  // admin can steal approvals made to factory
  const transferData = testERC20.interface.encodeFunctionData("transferFrom", [addr1.address, owner.address, ethers.utils.parseEther("1")]);
  await membershipFactory.callExternalContract(testERC20.address, transferData);

  let ownerBalanceAfter = await testERC20.balanceOf(owner.address);
  expect(ownerBalanceAfter.sub(ownerBalanceBefore)).to.equal(ethers.utils.parseEther("1"));

  // admin can mint/burn any DAO membership tokens
  const mintData = membershipERC1155.interface.encodeFunctionData("mint", [owner.address, 1, 100]);
  await membershipFactory.callExternalContract(nftAddress, mintData);

  let ownerBalanceERC1155 = await membershipERC1155.balanceOf(owner.address, 1);
  expect(ownerBalanceERC1155).to.equal(100);

  const burnData = membershipERC1155.interface.encodeFunctionData("burn", [owner.address, 1, 50]);
  await membershipFactory.callExternalContract(nftAddress, burnData);

  ownerBalanceERC1155 = await membershipERC1155.balanceOf(owner.address, 1);
  expect(ownerBalanceERC1155).to.equal(50);

  // admin can abuse approvals to any membership tokens as well
  await testERC20.connect(addr1).approve(membershipERC1155.address, ethers.utils.parseEther("1"));

  ownerBalanceBefore = await testERC20.balanceOf(owner.address);

  const data = membershipERC1155.interface.encodeFunctionData("callExternalContract", [testERC20.address, transferData]);
  await membershipFactory.callExternalContract(membershipERC1155.address, data);

  ownerBalanceAfter = await testERC20.balanceOf(owner.address);
  expect(ownerBalanceAfter.sub(ownerBalanceBefore)).to.equal(ethers.utils.parseEther("1"));
});
```

**Recommended Mitigation:** Implement restrictions on the target contracts and function selectors to be invoked by the arbitrary external calls to prevent abuse of the `MembershipFactory` contract ownership.

**One World Project:** The `EXTERNAL_CALLER` wallet is securely stored in AWS Secrets Manager in the backend, with no access granted to any individual. This wallet is necessary to execute on-chain transactions for off-chain processes. Further the executable functions are not defined to specific function-signatures, because in future this contract may be required to interact with contracts to distribute funds to projects or perform other tasks through the DAO, by executing through off-chain approvals

**Cyfrin:** Acknowledged. While AWS Secrets Manager adds security, private key or API key leaks remain a risk.

\clearpage
