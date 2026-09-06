---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: Meta transactions do not work with most of the calls in `MembershipFactory`
vuln_class: []
---

# Meta transactions do not work with most of the calls in `MembershipFactory`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** `MembershipFactory` uses a custom meta transactions implementation by inheriting `NativeMetaTransaction` which allow a relayer to pay the transaction fees on behalf of a user. This is achieved by following the same standard as ERC2771, where the user signs a transaction that is forwarded by a relayer and executed with the signing user's address appended to the `msg.data`.

Therefore, `msg.sender` cannot be used to retrieve the actual sender of a transaction as this will be the relayer in the case of [`NativeMetaTransaction::executeMetaTransaction`](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/meta-transaction/NativeMetaTransaction.sol#L33) being called. As already implemented [here](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L165-L185), the solution is to utilize a `_msgSender()` function that retrieves the signing user from the last 20 bytes of the `msg.data` in these cases.

For this reason, the following functions in `MembershipFactory` are problematic:
* `MembershipFactory::createNewDAOMembership` [[1](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L69), [2](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L84)].
* `MembershipFactory::joinDAO` [[1](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L129), [2](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L130), [3](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L131), [4](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L132)].
* `MembershipFactory::upgradeTier` [[1](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L141), [2](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L142), [3](https://github.com/OneWpOrg/audit-2024-10-oneworld/blob/416630e46ea6f0e9bd9bdd0aea6a48119d0b515a/contracts/dao/MembershipFactory.sol#L143)].

**Impact:** None of the above calls will work properly in combination when originated via `NativeMetaTransaction::executeMetaTransaction`, with `MembershipFactory::createNewDAOMembership` being the most problematic as it will create the DAO membership token with the `MembershipFactory` contract address as the `creator`. `MembershipFactory::joinDAO` and `MembershipFactory::upgradeTier` will most likely just revert as they require the `msg.sender` (`MembershipFactory`) to hold either `MembershipERC1155` tokens or payment `ERC20` tokens, which it shouldn't.

**Proof of Concept:** Test that can be added in `MembershipFactory.test.ts`:
```javascript
describe("Native meta transaction", function () {
  it("Meta transactions causes creation to use the wrong owner", async function () {
    await currencyManager.addCurrency(testERC20.address);

    const { chainId } = await ethers.provider.getNetwork();
    const salt = ethers.utils.hexZeroPad(ethers.utils.hexlify(chainId), 32)

    const domain = {
      name: 'OWP',
      version: '1',
      salt: salt,
      verifyingContract: membershipFactory.address,
    };
    const types = {
      MetaTransaction: [
        { name: 'nonce', type: 'uint256' },
        { name: 'from', type: 'address' },
        { name: 'functionSignature', type: 'bytes' },
      ],
    };
    const nonce = await membershipFactory.getNonce(addr1.address);
    const metaTransaction = {
      nonce,
      from: addr1.address,
      functionSignature: membershipFactory.interface.encodeFunctionData('createNewDAOMembership', [DAOConfig, TierConfig]),
    };
    const signature = await addr1._signTypedData(domain, types, metaTransaction);
    const {v,r,s} = ethers.utils.splitSignature(signature);

    const tx = await membershipFactory.executeMetaTransaction(metaTransaction.from, metaTransaction.functionSignature, r, s, v);
    const receipt = await tx.wait();
    const event = receipt.events.find((event:any) => event.event === "MembershipDAONFTCreated");
    const nftAddress = event.args[1];
    const creator = await MembershipERC1155.attach(nftAddress).creator();

    // creator becomes the membership factory not addr1
    expect(creator).to.equal(membershipFactory.address);
  });
});
```

**Recommended Mitigation:** Consider using `_msgSender()` instead of `msg.sender` in the above mentioned functions.

**One World Project:** The MetaTransaction’s only intended use is to call the callExternalContract function.The current implementation is that the `EXTERNAL_CALLER` signs the transaction in backend and then sends the signed object to the user and user sends it to the contract by the `executeMetaTransaction()` function. This way OWP Platform does not have to pay gas fees for any admin `transaction._msgSender()` still added at commit hash [`83ba905`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/83ba905f581be57a56d521deff6d75e0837b2237).

**Cyfrin:** Verified. `_msgSender()` is now used throughout the contract.
