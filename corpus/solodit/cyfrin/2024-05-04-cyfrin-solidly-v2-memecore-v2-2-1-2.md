---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-04-cyfrin-solidly-v2-memecore-v2-2-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-05-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md
tags:
- firm:cyfrin
- report:2024-05-04-cyfrin-solidly-v2-memecore-v2-2
title: '`SolidlyV2Pair::setPoolFee` fails to adequately consider fee setters defined
  by `SolidlyV2Factory`'
vuln_class: []
---

# `SolidlyV2Pair::setPoolFee` fails to adequately consider fee setters defined by `SolidlyV2Factory`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-04-cyfrin-solidly-v2-memecore-v2-2.md)_

---

**Description:** If a new `feeSetter` is registered by the owner of `SolidlyV2Factory`, then it is possible for the pool fee to be set below the minimum specified by the factory. This breaks the invariant that the pool fee should always be between the defined min/max values since it is only possible for the protocol to influence this value by explicitly modifying it on the factory itself, whereas a fee setter can modify it on the pool directly to become out of sync with the factory.

```solidity
function setPoolFee(uint16 _poolFee) external {
    require(ISolidlyV2Factory(factory).isFeeSetter(msg.sender) || msg.sender == copilot, 'UA');
    if (msg.sender == copilot) {
        require(_poolFee >= ISolidlyV2Factory(factory).minFee() && !copilotRevoked); // minimum fee enforced for copilot
    } else {
        require(!protocolRevoked);
    }
    require(_poolFee <= 1000); // pool fee capped at 10%
    uint16 feeOld = poolFee;
    poolFee = _poolFee;
    emit SetPoolFee(feeOld, _poolFee);
}
```

Additionally, if the owner of `SolidlyV2Factory` calls `SolidlyV2Pair::revokeFeeRole`, then registered fee setters are no longer able to call `SolidlyV2Pair::setPoolFee` despite no explicit consideration of fee setters.

**Impact:**
- The pool fee can become out of sync with `SolidlyV2Factory::minFee`.
- Fee setters cannot set fees once the protocol has revoked its fee role.

**Proof of Concept:**
```javascript
it("fee below min", async function () {
  const { user1, factory, pair } = await loadFixture(deploySolidlyV2Fixture);

  await factory.setFeeSetter(user1.address, true);
  pair.connect(user1).setPoolFee(0);
  await factory.minFee().then(minFee => console.log(`SolidlyV2Factory::minFee: ${minFee}`));
  await pair.poolFee().then(poolFee => console.log(`SolidlyV2Pair::poolFee: ${poolFee}`));

  await pair.revokeFeeRole();
  const minFee = await factory.minFee();
  await expect(pair.connect(user1).setPoolFee(minFee)).to.revertedWithoutReason();
});
```

**Recommended Mitigation:** Explicitly handle calls from fee setters as distinct from the factory owner in `SolidlyV2Pair::setPoolFee`, also enforcing that the pool fee cannot be set below the defined global minimum.

**Solidly Labs:** Acknowledged. Both these things are like this by design – `feeSetters` are not constrained by `minFee`, and both protocol and `feeSetter` are considered the same for revoke.

**Cyfrin:** Acknowledged.

\clearpage
