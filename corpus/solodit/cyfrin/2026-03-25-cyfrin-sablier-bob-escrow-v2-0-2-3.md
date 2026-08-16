---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Custom `comptroller` fees are ignored in `SablierBob::redeem`
vuln_class: []
---

# Custom `comptroller` fees are ignored in `SablierBob::redeem`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierComptroller::setCustomFeeUSDFor` allows `FEE_MANAGEMENT_ROLE` to set custom fees for a particular protocol (in this case the Bob protocol) and the user:
```solidity
function setCustomFeeUSDFor(
        Protocol protocol,
        address user,
        uint256 customFeeUSD
    )
        external
        override
        onlyRole(FEE_MANAGEMENT_ROLE)
        notExceedMaxFeeUSD(customFeeUSD)
    {
        ... ... ...

        // Effect: enable the custom fee, if it is not already enabled.
        if (!_protocolFees[protocol].customFeesUSD[user].enabled) {
            _protocolFees[protocol].customFeesUSD[user].enabled = true;
        }

        // Effect: update the custom fee for the provided protocol and user.
        _protocolFees[protocol].customFeesUSD[user].fee = customFeeUSD;

        ... ...  ...
```

However `SablierBob::redeem` utilizes `SablierComptroller::calculateMinFeeWei` which only considers the `minFeeUSD` member and ignores any custom fees configured, leading to lower or higher fees being collected from users than intended. This especially becomes problematic if certain users are expected to receive discounted or no fees due to other external factors/criteria:
```solidity
uint256 minFeeWei = comptroller.calculateMinFeeWei({ protocol: ISablierComptroller.Protocol.Bob });
```

**Recommended Mitigation:** Use `SablierComptroller::calculateMinFeeWeiFor` instead of `calculateMinFeeWei`.

**Sablier:** Acknowledged. This is an intentional design choice. We prefer to apply a global fee rather than adjusting fees on a per-user basis.

\clearpage
