---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-08-05-cyfrin-securitize-evm-async-vault-v2-0-3-3
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-08-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md
tags:
- firm:cyfrin
- report:2026-08-05-cyfrin-securitize-evm-async-vault-v2-0
title: Partial redemption claims require administrative recovery if the controller
  loses DS Token eligibility
vuln_class: []
---

# Partial redemption claims require administrative recovery if the controller loses DS Token eligibility

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-08-05-cyfrin-securitize-evm-async-vault-v2.0.md)_

---

**Description:** When a redemption generation is only partially fulfilled, `AsyncFundVault::redeem` and `AsyncFundVault::withdraw` perform two transfers atomically:

1. Transfer the fulfilled liquidity amount to `receiver`.
2. Return the unfulfilled DS Tokens to `controller`.

```solidity
if (totalLiquidity > 0) {
    $.liquidityToken.safeTransfer(receiver, totalLiquidity);
}

if (totalUnfulfilled > 0) {
    IERC20(address($.dsToken)).safeTransfer(
        controller,
        totalUnfulfilled
    );
}
```

The DS Token applies compliance checks to transfers. If the controller loses eligibility after requesting redemption but before claiming—for example, because of expired KYC, blacklisting, or wallet restrictions—the transfer of unfulfilled DS Tokens reverts.

**Impact:** A controller who loses DS Token eligibility cannot claim:
- The liquidity corresponding to the fulfilled part of the redemption.
- The DS Tokens corresponding to the unfulfilled part.

Recovery requires restoring the controller’s compliance status or intervention from `DEFAULT_ADMIN_ROLE` through `AsyncFundVaultAdmin::reassignClaimableRedemption` to move the claim to an eligible controller.

**Recommended Mitigation:** Document the required recovery procedure for controllers that lose DS Token eligibility.
Another option is to send DS tokens to the `receiver` instead of `controller`.

**Securitize:** Fixed in commit [a97c952](https://github.com/securitize-io/bc-async-ramp-sc/commit/a97c9525dccddd3f617e34956a68c12fb0bb595c).

**Cyfrin:** Verified.


\clearpage
