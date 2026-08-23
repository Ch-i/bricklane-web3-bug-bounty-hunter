---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-18-cyfrin-ondo-finance-0-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-04-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md
tags:
- firm:cyfrin
- report:2024-04-18-cyfrin-ondo-finance
title: Protocol may be short-changed by `BuidlRedeemer` during a USDC depeg event
vuln_class: []
---

# Protocol may be short-changed by `BuidlRedeemer` during a USDC depeg event

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-18-cyfrin-ondo-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-18-cyfrin-ondo-finance.md)_

---

**Description:** `OUSGInstantManager::_redeemBUIDL` assumes that 1 BUIDL = 1 USDC as it [enforces](https://github.com/ondoprotocol/rwa-internal/blob/6747ebada1c867a668a8da917aaaa7a0639a5b7a/contracts/ousg/ousgInstantManager.sol#L453-L459) receiving 1 USDC for every 1 BUIDL it redeems:
```solidity
uint256 usdcBalanceBefore = usdc.balanceOf(address(this));
buidl.approve(address(buidlRedeemer), buidlAmountToRedeem);
buidlRedeemer.redeem(buidlAmountToRedeem);
require(
  usdc.balanceOf(address(this)) == usdcBalanceBefore + buidlAmountToRedeem,
  "OUSGInstantManager::_redeemBUIDL: BUIDL:USDC not 1:1"
);
```
In the event of a USDC depeg (especially if the depeg is sustained), `BUIDLRedeemer` should return greater than a 1:1 ratio since 1 USDC would not be worth $1, hence 1 BUIDL != 1 USDC meaning the value of the protocol's BUIDL is worth more USDC. However `BUIDLReceiver` does not do this, it only ever [returns](https://etherscan.io/address/0x9ba14Ce55d7a508A9bB7D50224f0EB91745744b7#code) 1:1.

**Impact:** In the event of a USDC depeg the protocol will be short-changed by `BuidlRedeemer` since it will happily receive only 1 USDC for every 1 BUIDL redeemed, even though the value of 1 BUIDL would be greater than the value of 1 USDC due to the USDC depeg.

**Recommended Mitigation:** To prevent this situation the protocol would need to use an oracle to check whether USDC had depegged and if so, calculate the amount of USDC it should receive in exchange for its BUIDL. If it is short-changed it would either have to revert preventing redemptions or allow the redemption while saving the short-changed amount to storage then implement an off-chain process with BlackRock to receive the short-changed amount.

Alternatively the protocol may simply accept this as a risk to the protocol that it will be willingly short-changed during a USDC depeg in order to allow redemptions to continue.

**Ondo:**
Fixed in commits [408bff1](https://github.com/ondoprotocol/rwa-internal/commit/408bff112c39f393f67dde6c30a6addf3b221ee9), [8a9cae9](https://github.com/ondoprotocol/rwa-internal/commit/8a9cae9af5787f06db42b4224b147d60493e0133). We now use Chainlink USDC/USD Oracle and if USDC depegs below our tolerated minimum value both minting and redemptions will be stopped.

**Cyfrin:** Verified.

\clearpage
