---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-10-17-carina-finance-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-10-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-17-Carina-Finance.md
tags:
- firm:codespect
- report:2025-10-17-carina-finance
title: '[I-01] EIP-1271 signature verification allows for a callback to user-controlled
  contracts'
vuln_class: []
---

# [I-01] EIP-1271 signature verification allows for a callback to user-controlled contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-10-17-Carina-Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-10-17-Carina-Finance.md)_

---

**Files:** [`mixins/OrderSigning.sol`](https://github.com/carina-finance/carina-sc/blob/6ff2ad112b6b62acb054411b8181d9414970b08b//src/mixins/OrderSigning.sol#L208-L210)

**Description:**

The settlement process, initiated by a Solver’s call to the `settle(...)` function, involves verifying user signatures for each trade. The protocol supports various signing schemes, including EIP-1271 for smart contract-based wallets. The verification for this scheme is handled in the `recoverEIP1271Signer(...)` function.

This function makes an external call to the user’s contract to invoke `isValidSignature(...)`, as required by the EIP-1271 standard. This callback occurs after the pre-settlement actions (`actions[0]`) have been executed but before the main liquidity-providing actions (`actions[1]`) and the final token transfers.

This creates an attack surface where a malicious user, via their smart contract wallet, can execute arbitrary logic during the settlement process. This could be used to manipulate the state of external protocols (e.g., AMM pool prices) that the Solver’s actions rely on. Such manipulation could lead to outcomes like transaction reverts due to slippage (denial of service against the Solver) or achieving a more favorable trade execution for the user at the Solver’s expense.

```solidity
// src/mixins/OrderSigning.sol

function recoverEip1271Signer(bytes32 orderDigest, bytes calldata encodedSignature)
    internal
    view
    returns (address owner)
{
    assembly {
        // owner = address(encodedSignature[0:20])
        owner := shr(96, calldataload(encodedSignature.offset))
    }

    bytes calldata signature = encodedSignature[20:];

    // @audit-issue This makes an arbitrary external call to a user-controlled contract.
    // It executes between the pre-settlement (setup) and main settlement actions.
    if (IEIP1271(owner).isValidSignature(orderDigest, signature) != EIP1271_MAGIC_VALUE) {
        revert InvalidEip1271Signature();
    }
}
```

Unlike traditional front-running, the logic that affects the Solver is encoded into the order’s own verification process via the smart contract wallet. This means that private mempools and other front-running protections are ineffective against this vector.

**Impact:** This issue is informational, as the behaviour is part of a standard integration. It aims to highlight the potential risk for Solvers, who are the primary actors exposed to this manipulation vector.

**Recommendation:** Consider documenting this behaviour to ensure that Solvers are aware of the potential for re-entrancy through EIP-1271 signature verification. Solvers should implement their own safeguards, such as performing pre-flight checks on external conditions and setting strict slippage parameters within their settlement actions to mitigate manipulation risk.

**Status:** Acknowledged

**Client response:** We acknowledge it and will document it in the solver integration guide for Carina.
