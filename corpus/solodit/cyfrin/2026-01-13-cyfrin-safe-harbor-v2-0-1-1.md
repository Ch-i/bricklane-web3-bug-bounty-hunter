---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-13-cyfrin-safe-harbor-v2-0-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-13-cyfrin-safe-harbor-v2-0
title: Missing validation allows empty account addresses in agreement scope, creating
  ambiguous whitehat coverage
vuln_class: []
---

# Missing validation allows empty account addresses in agreement scope, creating ambiguous whitehat coverage

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-13-cyfrin-safe-harbor-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-13-cyfrin-safe-harbor-v2.0.md)_

---

**Description:** The `Agreement::_validateChains` validates that the accounts array is non-empty but does not validate the contents of individual `Account` structs. This allows accounts with empty `accountAddress` strings to be added to agreements.

Note that `assetRecoveryAddress` is validated for non-empty strings, but the same validation is not applied to `accountAddress` within each account.

**Impact:** A protocol could accidentally deploy an agreement that appears valid but provides no actual scope definition, rendering the Safe Harbor adoption ineffective. Also, when querying the Safe Harbor Registry, whitehats cannot determine if an empty account address represents "all addresses" or "no addresses".

**Proof of Concept:** Add this test to `AgreementTest.t.sol`:

```solidity
   function test_POC_emptyAccountAddressAllowed() public {
        // Create account with empty address
        SHAccount[] memory accounts = new SHAccount[](1);
        accounts[0] = SHAccount({
            accountAddress: "",  // Empty!
            childContractScope: ChildContractScope.All
        });

        SHChain[] memory chains = new SHChain[](1);
        chains[0] = SHChain({
            assetRecoveryAddress: "0x742d35Cc6634C0532925a3b844Bc454e",
            accounts: accounts,
            caip2ChainId: "eip155:56"
        });

        vm.prank(owner);
        agreement.addChains(chains); //@note this does not revert

        // Verify empty account was added
        AgreementDetails memory details = agreement.getDetails();

        bool foundBscChain = false;
        for (uint256 i = 0; i < details.chains.length; i++) {
            if (keccak256(bytes(details.chains[i].caip2ChainId)) == keccak256(bytes("eip155:56"))) {
                foundBscChain = true;
                assertEq(details.chains[i].accounts.length, 1);
                assertEq(details.chains[i].accounts[0].accountAddress, "");
                break;
            }
        }
        assertTrue(foundBscChain, "BSC chain not found");
    }
```


**Recommended Mitigation:** Consider adding validation for individual account addresses within `_validateChains`, consistent with the existing validation for `assetRecoveryAddress`.

**SafeHarbor:**
Fixed in [e32dd76](https://github.com/PatrickAlphaC/safe-harbor/commit/e32dd768c48b72b3cfe72a17676e6348c6da1837) and [a881fdc](https://github.com/PatrickAlphaC/safe-harbor/commit/a881fdc10a19364c36c92b15e10d74e0143a291b).

**Cyfrin:** Verified.
