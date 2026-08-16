---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: Missing mode field validation in walletclient allows handler selection via
  untrusted input
vuln_class: []
---

# Missing mode field validation in walletclient allows handler selection via untrusted input

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `WalletClient.connect()` method in `wallet-client/src/client.ts` uses the dApp-provided `sessionRequest.mode` field to select between `TrustedConnectionHandler` (no OTP) and `UntrustedConnectionHandler` (OTP required) without any input validation:

```js
const handler: IConnectionHandler = request.mode === "trusted"
  ? new TrustedConnectionHandler(context)
  : new UntrustedConnectionHandler(context);
```

The `mode` field originates entirely from the dApp side (`dapp-client/src/client.ts`) and is embedded directly into the `SessionRequest` transmitted via QR code or deeplink. No runtime enum check, type guard, or wallet-side policy enforcement exists before handler selection.

**Impact:** In MetaMask's actual deployments, this has **no practical impact** as:
- **connect-monorepo** (`connect-multichain/src/multichain/transports/mwp/index.ts`) hard-codes `mode: 'trusted'` so the dApp can never controls this value.
- **MetaMask Mobile** (`SDKConnect/handlers/handleConnectionReady.ts`) ignores the `mode` field entirely and enforces its own OTP policy based on `connection.origin` and `lastAuthorized`.

However, any **third-party wallet** integrating the raw `WalletClient` library without implementing independent security policy would allow a malicious dApp to set `mode: 'trusted'` and skip OTP verification entirely. This is a defense-in-depth gap in the library's public API.

**Recommended Mitigation:** Add runtime validation of the `mode` field before handler selection in `WalletClient.connect()`:

```js
if (!["trusted", "untrusted"].includes(request.mode)) {
  throw new SessionError(ErrorCode.INVALID_PARAM, `Invalid connection mode: ${request.mode}`);
}
```

Ideally, the wallet should not rely on the dApp-provided `mode` at all. Consider allowing wallet integrators to override or enforce mode via a configuration option (e.g., `WalletClient({ forceUntrusted: true })`), so the security decision stays on the wallet side.

**MetaMask:** Fixed in commit [4c8bf8](https://github.com/MetaMask/mobile-wallet-protocol/commit/4c8bf8564ab1190e37f8b47769534445b88fe2d6).

**Cyfrin:** Verified.
