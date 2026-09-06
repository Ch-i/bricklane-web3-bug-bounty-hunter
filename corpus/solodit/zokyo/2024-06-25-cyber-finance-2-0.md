---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-06-25-cyber-finance-2-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-06-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md
tags:
- firm:zokyo
- report:2024-06-25-cyber-finance
title: PUSH0 Opcode is Incompatible with some Chains
vuln_class: []
---

# PUSH0 Opcode is Incompatible with some Chains

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-06-25-Cyber Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-25-Cyber%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Description**

The `CyberFinance` contract is written using Solidity version 0.8.21, which introduces the push0 opcode. This opcode is not supported by all chains, especially those not compatible with the Shanghai hardfork. Deploying this contract on such incompatible chains could lead to deployment failures.

This means that the produced bytecode won't be compatible with the chains that don't yet support the Shanghai hard fork. This could also become a problem if different versions of Solidity are used to compile contracts for different chains. The differences in bytecode between versions can impact the deterministic nature of contract addresses.


**Recommendation**: 

To ensure broader compatibility and prevent deployment issues, it is recommended to either roll back the Solidity version or hardcode the EVM version to "paris" in the Foundry configuration file (foundry.toml).
