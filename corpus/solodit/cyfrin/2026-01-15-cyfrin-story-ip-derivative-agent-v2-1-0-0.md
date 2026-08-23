---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-15-cyfrin-story-ip-derivative-agent-v2-1-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-15T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md
tags:
- firm:cyfrin
- report:2026-01-15-cyfrin-story-ip-derivative-agent-v2-1
title: Actual minting fee can differ from predicted fee
vuln_class: []
---

# Actual minting fee can differ from predicted fee

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-15-cyfrin-story-ip-derivative-agent-v2.1.md)_

---

**Description:** `IPDerivativeAgent::registerDerivativeViaAgent` relies on `predictMintingLicenseFee(...)` to determine `tokenAmount`, transfers that amount from the caller, and approves the Royalty Module for exactly that amount. However, the fee ultimately paid during `registerDerivative(...)` may differ from the predicted value (e.g., due to hook logic or other execution-time conditions). The agent does not reconcile the predicted amount with the actual amount spent.

**Impact:**
- If the actual fee is higher than the predicted amount, the Royalty Module may attempt to pull more than the agent approved/holds, causing `registerDerivative(...)` to revert (DoS) despite the user providing a sufficiently high `maxMintingFee`.
- If the actual fee is lower than the predicted amount, the excess tokens remain in the agent contract with no automatic refund path, potentially leading to stranded user funds (recoverable only via privileged/admin withdrawal, if at all).

**Recommended mitigation:**
Consider approving (and fund) `maxMintingFee`, then refund any remaining token balance to the caller after a successful registration:

```diff

        // Handle token payment if required
        if (currencyToken != address(0) && tokenAmount > 0) {
            IERC20 token = IERC20(currencyToken);

            // Transfer tokens from licensee to this contract
            token.safeTransferFrom(msg.sender, address(this), tokenAmount);

            // Increase allowance for RoyaltyModule to pull tokens during registerDerivative
+           token.safeIncreaseAllowance(ROYALTY_MODULE, maxMintingFee);
-           token.safeIncreaseAllowance(ROYALTY_MODULE, tokenAmount);
        }

        // ...

        // Clean up any remaining allowance for RoyaltyModule
        if (currencyToken != address(0) && tokenAmount > 0) {
            IERC20 token = IERC20(currencyToken);
            uint256 remainingAllowance = token.allowance(address(this), ROYALTY_MODULE);
            if (remainingAllowance > 0) {
+               token.safeTransfer(msg.sender, token.balanceOf(address(this)));
                token.forceApprove(ROYALTY_MODULE, 0);
            }
        }

```

**Story:** Fixed in [PR#5](https://github.com/piplabs/story-ecosystem/pull/5)

**Cyfrin:** Verified. Allowance is done for `maxMintingFee` together with transfer to the agent. Left over tokens are then returned after the call to the license module.

\clearpage
