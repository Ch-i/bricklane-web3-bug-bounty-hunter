---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-5-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: Discarded return data from low-level `.call{value:}` should use inline-assembly
  `call`
vuln_class: []
---

# Discarded return data from low-level `.call{value:}` should use inline-assembly `call`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Two payable transfer paths use `(bool ok,) = recipient.call{value: amount}("")` to forward ETH and discard the return data. The high-level `.call` path always copies any returndata into memory before discarding it, wasting gas on the copy and exposing the caller to a return-bomb DoS where the recipient returns a huge payload to inflate caller memory expansion costs. Replace with assembly `call(gas(), to, value, 0, 0, 0, 0)` so the EVM never copies returndata.

```solidity
src/OnChainLab.sol
311:        (bool success,) = to.call{value: amount}("");
312:        if (!success) revert WithdrawFailed();

src/NFT/LabNFT.sol
162:        (bool success,) = payable(msg.sender).call{value: balance}("");
163:        if (!success) revert WithdrawFailed();
```

**Recommended Mitigation:** Use inline assembly to avoid the returndata copy:

```solidity
bool success;
assembly {
    success := call(gas(), to, amount, 0, 0, 0, 0)
}
if (!success) revert WithdrawFailed();
```

`OnChainLab::withdraw` is on the user/EntryPoint hot path; `LabNFT::withdraw` is admin-only (cold) but inherits the same return-bomb surface, so we report them together.

**Molecule:** Fixed in commit [93d2e5e](https://github.com/moleculeprotocol/onchainlabs/commit/93d2e5e).

**Cyfrin:** Verified.
