---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-11-cyfrin-wormhole-evm-ntt-v2-4-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-04-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md
tags:
- firm:cyfrin
- report:2024-04-11-cyfrin-wormhole-evm-ntt-v2
title: Unnecessary stack variable in `Governance::encodeGeneralPurposeGovernanceMessage`
vuln_class: []
---

# Unnecessary stack variable in `Governance::encodeGeneralPurposeGovernanceMessage`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-11-cyfrin-wormhole-evm-ntt-v2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-11-cyfrin-wormhole-evm-ntt-v2.md)_

---

[`Governance::encodeGeneralPurposeGovernanceMessage`](https://github.com/wormhole-foundation/example-native-token-transfers/blob/f4e2277b358349dbfb8a654d19a925628d48a8af/evm/src/wormhole/Governance.sol#L126-L144) currently assigns the stack variable `callDataLength`; however, this is not necessary as the (already checked) downcast can be performed directly within the subsequent packed encoding.

```solidity
function encodeGeneralPurposeGovernanceMessage(GeneralPurposeGovernanceMessage memory m)
    public
    pure
    returns (bytes memory encoded)
{
    if (m.callData.length > type(uint16).max) {
        revert PayloadTooLong(m.callData.length);
    }
    uint16 callDataLength = uint16(m.callData.length);
    return abi.encodePacked(
        MODULE,
        m.action,
        m.chain,
        m.governanceContract,
        m.governedContract,
        callDataLength,
        m.callData
    );
}
```

Consider removing this stack variable to save gas.

**Wormhole Foundation:** This is used as a view and is not called internally, so gas is not a concern.

**Cyfrin:** Acknowledged.
