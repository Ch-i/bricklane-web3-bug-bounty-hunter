---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-11-06-cyfrin-securitize-global-registry-v2-0-1-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-11-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md
tags:
- firm:cyfrin
- report:2025-11-06-cyfrin-securitize-global-registry-v2-0
title: '`StandardToken::transferWithPermit` can be DoS attacked by front-running to
  directly call `ERC20PermitMixin::permit`'
vuln_class: []
---

# `StandardToken::transferWithPermit` can be DoS attacked by front-running to directly call `ERC20PermitMixin::permit`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-11-06-cyfrin-securitize-global-registry-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-06-cyfrin-securitize-global-registry-v2.0.md)_

---

**Description:** `StandardToken::transferWithPermit` contains two calls:
* first to `ERC20PermitMixin::permit`
* second to the `StandardToken::transferFrom`

**Impact:** Since the permit signature and parameters are visible in the mempool before execution, an attacker can extract these values and front-run the transaction by directly calling `StandardToken::permit`. This consumes the user's nonce causing the original call `StandardToken::transferWithPermit` to revert, making it impossible to atomically grant the approval and transfer the tokens.

**Proof of concept**
Run the PoC in `dstoken-regulated.test.ts` inside the `describe('Permit transfer', async function () {`:
```typescript
it('front-running attack on transferWithPermit()', async () => {
        const [owner, spender, recipient, attacker] = await hre.ethers.getSigners();
        const { dsToken, registryService } = await loadFixture(deployDSTokenRegulated);
        const value = 100;
        const deadline = BigInt(Math.floor(Date.now() / 1000) + 3600);

        // Owner creates a signature to allow spender to transfer tokens to recipient
        const message = {
          owner: owner.address,
          spender: spender.address,
          value,
          nonce: await dsToken.nonces(owner.address),
          deadline,
        };
        const { v, r, s } = await buildPermitSignature(owner, message, await dsToken.name(), await dsToken.getAddress());

        // Register investors and issue tokens to owner; see that the attacker is not even an ibnvestor so it could be any address
        await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_1, owner, registryService);
        await registerInvestor(INVESTORS.INVESTOR_ID.INVESTOR_ID_2, recipient, registryService);

        await dsToken.issueTokens(owner, value);

        // ATTACK SCENARIO 1: Attacker front-runs by calling permit() directly
        await dsToken.connect(attacker).permit(owner.address, spender.address, value, deadline, v, r, s);


        // When the original transferWithPermit() executes, it FAILS
        // because the nonce has already been used
        await expect(
          dsToken.connect(spender).transferWithPermit(owner.address, recipient.address, value, deadline, v, r, s)
        ).to.be.revertedWith('Permit: invalid signature');
      });
```

**Recommended Mitigation:** Use the try and catch pattern:
```solidity
function transferWithPermit(
    address from,
    address to,
    uint256 value,
    uint256 deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
) external returns (bool) {
    // Try to execute permit, but don't revert if it fails
    try this.permit(from, msg.sender, value, deadline, v, r, s) {
        // Permit succeeded
    } catch {
        // Permit failed (possibly due to front-running or already executed)
        // Verify we have sufficient allowance to proceed
        require(allowance(from, msg.sender) >= value, "Insufficient allowance");
    }

    // Perform the actual transferFrom
    return transferFrom(from, to, value);
}
```

**Securitize:** Fixed in commit [d7cf385](https://github.com/securitize-io/dstoken/commit/d7cf3858c371def66e5b37ed0949aa991d0a0234).

**Cyfrin:** Verified.
