---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1-2-20
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-10-cyfrin-securitize-dstoken-rebasing-v2-1
title: Investor can prevent themselves from being removed by making `removeInvestor`
  revert
vuln_class: []
---

# Investor can prevent themselves from being removed by making `removeInvestor` revert

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-10-cyfrin-securitize-dstoken-rebasing-v2.1.md)_

---

**Description:** The `removeInvestor` function in `RegistryService.sol` contains a flaw that allows any investor to permanently prevent their removal from the system. The function requires that `investors[_id].walletCount == 0` before allowing investor removal, but investors can add unlimited wallets via `addWalletByInvestor` without any restrictions, while only `EXCHANGE` roles can remove wallets via `removeWallet`.

```solidity
function removeInvestor(string calldata _id) public override onlyExchangeOrAbove investorExists(_id) returns (bool) {
        require(getTrustService().getRole(msg.sender) != EXCHANGE || investors[_id].creator == msg.sender, "Insufficient permissions");
        require(investors[_id].walletCount == 0, "Investor has wallets"); <----------

        for (uint8 index = 0; index < 16; index++) {
            delete attributes[_id][index];
        }

        delete investors[_id];

        emit DSRegistryServiceInvestorRemoved(_id, msg.sender);

        return true;
    }
```

This creates a permanent DoS condition where malicious investors can add wallets to prevent their own removal

**Impact:** `removeInvestor` can be DoS, making an investor unremovable.

**Recommended Mitigation:** Consider removing `addWalletByInvestor`.

**Securitize:** Fixed in commit [05c5bad](https://github.com/securitize-io/dstoken/commit/05c5bada3c2801b1333fc96f4abc5226a84471f0) by removing `addWalletByInvestor`.

**Cyfrin:** Verified.
