---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-12-cyfrin-molecule-onchainlab-v2-0-4-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-12-cyfrin-molecule-onchainlab-v2-0
title: '`OnChainLab::execute` discards `ExecLib::execute` return data'
vuln_class: []
---

# `OnChainLab::execute` discards `ExecLib::execute` return data

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-12-cyfrin-molecule-onchainlab-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-12-cyfrin-molecule-onchainlab-v2.0.md)_

---

**Description:** Two `execute` overloads on `OnChainLab` invoke `ExecLib::execute` but do not capture or surface the return value. ERC-4337 callers that route their UserOps through these entry points cannot retrieve the call's return data, even though `ExecLib::execute(address,uint256,bytes)` returns `bytes memory result` and `ExecLib::execute(ExecMode, bytes)` returns `bytes[] memory returnData`. Compare with the ERC-6551 overload (line 253) which returns `bytes memory result` and the ERC-7579 fallback dispatch (line 232-234) which assembly-returns the call's result data.

```solidity
src/OnChainLab.sol
285:    function execute(address to, uint256 value, bytes calldata data) external payable onlyEntryPointOrOwner {
286:        state++;
287:        emit StateUpdated(state);
288:        ExecLib.execute(to, value, data);
289:    }
...
298:    function execute(ExecMode execMode, bytes calldata executionCalldata) external payable onlyEntryPoint {
299:        state++;
300:        emit StateUpdated(state);
301:        ExecLib.execute(execMode, executionCalldata);
302:    }
```

**Recommended Mitigation:** Either capture and return the data (preferred - matches the other overload), or document explicitly in NatSpec that this entrypoint deliberately returns nothing. Returning the data is a pure win for ERC-4337 callers that want to inspect inner-call results.

```solidity
function execute(address to, uint256 value, bytes calldata data)
    external payable onlyEntryPointOrOwner
    returns (bytes memory result)
{
    state++;
    emit StateUpdated(state);
    result = ExecLib.execute(to, value, data);
}
```

**Molecule:** Fixed in commit [41aac79](https://github.com/moleculeprotocol/onchainlabs/commit/41aac79).

**Cyfrin:** Verified.
