---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Extract logic for the last element when looping over Stems in `EnrootFacet::enrootDeposits`
vuln_class: []
---

# Extract logic for the last element when looping over Stems in `EnrootFacet::enrootDeposits`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, the `i+1 == stems.length` [condition](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/EnrootFacet.sol#L139) is checked during each iteration when looping over Stems in `EnrootFacet::enrootDeposits`. This can be modified to save gas, as shown below:

```diff
// EnrootFacet::enrootDeposits
//...
+       uint256 stemsLengthMinusOne = stems.length - 1;
-       for (uint256 i; i < stems.length; ++i) {
+       for (uint256 i; i < stems.stemsLengthMinusOne; ++i) {
-           if (i+1 == stems.length) {
-               // Ensure that a rounding error does not occur by using the
-               // remainder BDV for the last Deposit.
-               depositBdv = newTotalBdv.sub(bdvAdded);
-           } else {
                // depositBdv is a proportional amount of the total bdv.
                // Cheaper than calling the BDV function multiple times.
                depositBdv = amounts[i].mul(newTotalBdv).div(ar.tokensRemoved);
-           }
            LibTokenSilo.addDepositToAccount(
                msg.sender,
                token,
                stems[i],
                amounts[i],
                depositBdv,
                LibTokenSilo.Transfer.noEmitTransferSingle
            );

            stalkAdded = stalkAdded.add(
                depositBdv.mul(_stalkPerBdv).add(
                    LibSilo.stalkReward(
                        stems[i],
                        _lastStem,
                        uint128(depositBdv)
                    )
                )
            );

            bdvAdded = bdvAdded.add(depositBdv);
        }
+       depositBdv = newTotalBdv.sub(bdvAdded);
+       LibTokenSilo.addDepositToAccount(
+           msg.sender,
+           token,
+           stems[stemsLengthMinusOne],
+           amounts[stemsLengthMinusOne],
+           depositBdv,
+           LibTokenSilo.Transfer.noEmitTransferSingle
+       );
+
+       stalkAdded = stalkAdded.add(
+           depositBdv.mul(_stalkPerBdv).add(
+               LibSilo.stalkReward(
+                   stems[stemsLengthMinusOne],
+                   _lastStem,
+                   uint128(depositBdv)
+               )
+           )
+       );
+
+       bdvAdded = bdvAdded.add(depositBdv);
//...
```
