---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-05-cyfrin-metamask-connect-v2-0-2-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-05T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-05-cyfrin-metamask-connect-v2-0
title: OTP generated using math.random is not cryptographically secure way to generate
  verification code
vuln_class: []
---

# OTP generated using math.random is not cryptographically secure way to generate verification code

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-05-cyfrin-metamask-connect-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-05-cyfrin-metamask-connect-v2.0.md)_

---

**Description:** The `untrusted` connection flow is the protocol's high-security path. It is designed for cross-device scenarios (e.g., scanning a QR code from an untrusted computer) where a man-in-the-middle could subscribe to the handshake channel and race the legitimate dApp. In this flow, the One-Time Password is the sole mechanism that authenticates the two parties to each other,  the user visually compares the OTP displayed on the wallet screen to the one presented by the dApp.
```js
// packages/wallet-client/src/handlers/untrusted-connection-handler.ts:49-53
private _generateOtpWithDeadline(): { otp: string; deadline: number } {
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const deadline = Date.now() + this.otpTimeoutMs;
    return { otp, deadline };
}
```

The same non-cryptographic pattern is also used in the legacy V1 OTP generator on the `metamask-mobile` side:
```js
// metamask-mobile/app/core/SDKConnect/utils/generateOTP.util.ts:1-2
const generateRandomIntegerInRange = (min: number, max: number): number =>
  Math.floor(Math.random() * (max - min + 1)) + min;
```

`Math.random()` is explicitly defined by the `ECMAScript` specification as [not providing cryptographically secure random numbers](https://deepsource.com/blog/dont-use-math-random). Every modern JavaScript engine implements it with `xorshift128+`, a fast but fully deterministic PRNG. Its full 128-bit internal state can be reconstructed from a handful of observed outputs using known algebraic techniques (e.g., Z3 constraint solving).

In React native's `JavaScriptCore` and `Hermes` engines, the `PRNG` state is shared across the entire JS execution context, meaning any call to Math.random() anywhere in the application animation timing, layout jitter, analytics sampling advances the same state and provides useful observations to an attacker who can instrument or observe the execution.

**Impact:** Because the OTP is the only authentication factor in the untrusted handshake, predictability here could the entire security model of the cross-device flow. The OTP search space is already limited to `900,000` possible values (six-digit codes from `100000` to `999999`), and the dApp allows 3 guesses (`this.otpAttempts = 3`), giving a blind brute-force a `1-in-300,000` chance per connection.

With PRNG state recovery (feasible from approximately 3–4 prior `Math.random() `observations from the same context), an attacker can predict the exact OTP with certainty, enabling a complete man-in-the-middle of the key exchange.

On the dApp side, the OTP verification itself also uses a direct string comparison rather than a timing-safe comparison:
```js
// packages/dapp-client/src/handlers/untrusted-connection-handler.ts:93
if (otp !== offer.otp) {
```
While this comparison between short strings and practical timing extraction is `difficult over a WebSocket`, it compounds the weak generation with a weak verification pattern.

**Recommended Mitigation:** Replace `Math.random()` with the Web Crypto API's `crypto.getRandomValues()`, which is backed by the operating system's `CSPRNG` and is available in all target environments (browser, React Native, Node.js):
```js
private _generateOtpWithDeadline(): { otp: string; deadline: number } {
    const buf = new Uint32Array(1);
    crypto.getRandomValues(buf);
    const otp = (100000 + (buf[0] % 900000)).toString();
    const deadline = Date.now() + this.otpTimeoutMs;
    return { otp, deadline };
}
```

Additionally, consider using a timing-safe comparison for OTP verification on the dApp side, and consider rate-limiting OTP attempts at the protocol level rather than relying solely on a client-side counter.

**MetaMask:** Fixed in commits [46f81](https://github.com/MetaMask/mobile-wallet-protocol/commit/46f8111c151484d44992ced7bc5cd24307ab7930) , [7bbacf](https://github.com/MetaMask/mobile-wallet-protocol/commit/7bbacf3a17fa6d362ac4f29df5158e17ff34513d).

**Cyfrin:** Verified
