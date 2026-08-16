---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-09-cyfrin-wormhole-evm-cctp-v2-1-2-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md
tags:
- firm:cyfrin
- report:2024-04-09-cyfrin-wormhole-evm-cctp-v2-1
title: Use `SafeERC20::safeIncreaseAllowance` in the place of `IERC20::approve` in
  `WormholeCctpTokenMessenger::setTokenMessengerApproval`
vuln_class: []
---

# Use `SafeERC20::safeIncreaseAllowance` in the place of `IERC20::approve` in `WormholeCctpTokenMessenger::setTokenMessengerApproval`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-09-cyfrin-wormhole-evm-cctp-v2-1.md)_

---

Although the `SafeERC20` library is [declared](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/bbc593d7f4caf2b59bf9de18a870e2df37ed6fd4/evm/src/contracts/WormholeCctpTokenMessenger.sol#L26) as being used for the `IERC20` interface, [`WormholeCctpTokenMessenger::setTokenMessengerApproval`](https://github.com/wormhole-foundation/wormhole-circle-integration/blob/bbc593d7f4caf2b59bf9de18a870e2df37ed6fd4/evm/src/contracts/WormholeCctpTokenMessenger.sol#L92-L98) uses `IERC20::approve` directly instead of `SafeERC20::safeApprove`. Whilst the `FiatTokenV2_2` implementation of `IERC20::approve` does return the `true` boolean, reverting otherwise, some tokens can silently fail when this function is called; therefore, it may be necessary to check the return value of this call if the protocol ever intends to work with other ERC20 tokens. Also, note that OpenZeppelin discourages the use of `SafeERC20::safeApprove` (deprecated in v5) and instead recommends the use of `safeERC20::safeIncreaseAllowance`.

**Wormhole Foundation:** Fixed in [PR \#52](https://github.com/wormhole-foundation/wormhole-circle-integration/pull/52).

**Cyfrin:** Verified. The direct use of `ERC20::approve` has been modified to instead use `safeERC20::safeIncreaseAllowance`.
