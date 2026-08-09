---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Consolidate unnecessary code duplication in `ConvertFacet::_withdrawTokens`
vuln_class: []
---

# Consolidate unnecessary code duplication in `ConvertFacet::_withdrawTokens`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`ConvertFacet::_withdrawTokens` duplicates the following code in [L119-132](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L119-L132) then again in [L137-151](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L137-L151):

```solidity
if (a.tokensRemoved.add(amounts[i]) < maxTokens) {
    //keeping track of stalk removed must happen before we actually remove the deposit
    //this is because LibTokenSilo.grownStalkForDeposit() uses the current deposit info
    // @audit start duplicated code
    depositBDV = LibTokenSilo.removeDepositFromAccount(
        msg.sender,
        token,
        stems[i],
        amounts[i]
    );
    bdvsRemoved[i] = depositBDV;
    a.stalkRemoved = a.stalkRemoved.add(
        LibSilo.stalkReward(
            stems[i],
            LibTokenSilo.stemTipForToken(token),
            depositBDV.toUint128()
        )
    );
    // @audit end duplicated code

} else {
    amounts[i] = maxTokens.sub(a.tokensRemoved);

    // @audit start duplicated code
    depositBDV = LibTokenSilo.removeDepositFromAccount(
        msg.sender,
        token,
        stems[i],
        amounts[i]
    );

    bdvsRemoved[i] = depositBDV;
    a.stalkRemoved = a.stalkRemoved.add(
        LibSilo.stalkReward(
            stems[i],
        LibTokenSilo.stemTipForToken(token),
            depositBDV.toUint128()
        )
    );
    // @audit end duplicated code
}
```

Consider refactoring to remove the duplicated code by changing the `if` condition to only update `amounts[i]` when required then perform the same processing that is currently on each `if/else` branch:

```solidity
while ((i < stems.length) && (a.tokensRemoved < maxTokens)) {
    if (a.tokensRemoved.add(amounts[i]) >= maxTokens) {
        amounts[i] = maxTokens.sub(a.tokensRemoved);
    }

    //keeping track of stalk removed must happen before we actually remove the deposit
    //this is because LibTokenSilo.grownStalkForDeposit() uses the current deposit info
    depositBDV = LibTokenSilo.removeDepositFromAccount(
        msg.sender,
        token,
        stems[i],
        amounts[i]
    );
    bdvsRemoved[i] = depositBDV;
    a.stalkRemoved = a.stalkRemoved.add(
        LibSilo.stalkReward(
            stems[i],
            LibTokenSilo.stemTipForToken(token),
            depositBDV.toUint128()
        )
    );

    a.tokensRemoved = a.tokensRemoved.add(amounts[i]);
    a.bdvRemoved = a.bdvRemoved.add(depositBDV);

    depositIds[i] = uint256(LibBytes.packAddressAndStem(token, stems[i]));
    i++;
}
```


\clearpage
