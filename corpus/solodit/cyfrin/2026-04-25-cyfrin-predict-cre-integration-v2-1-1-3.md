---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Missing CRE-side runtime validation of config values before use
vuln_class: []
---

# Missing CRE-side runtime validation of config values before use

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** Grouping of off-chain / CRE-side defensive-depth gaps where TypeScript workflow code, init scripts, or config files pass values into critical operations (settlement calls, chain-scoped deploy actions) without validating that those values are within acceptable bounds at runtime. In every case the consequence is operator-footgun: a misconfiguration silently produces wrong behaviour rather than failing loudly.

---

**1. CRE `runtime.config` lacks runtime validation**

The CRE TypeScript workflow defines a `Config` type in `types.ts` that provides compile-time structural typing for config fields (`dataStreamsEndpoint`, `adapterAddress`, `intervals[]`, `gasLimit`). TypeScript types are erased at runtime and do not validate the actual JSON values loaded from `config.*.json` during execution. No runtime schema validation, semantic boundary checks, or domain-pinning assertions are applied before these values flow into critical operations.

**Impact:** An invalid config value silently passes type-check at build time, then produces runtime failures (dead calls, reverts, silent settlement stalls) that are hard to diagnose because no input-validation layer exists to reject the bad value at the boundary.

**Recommended:** Add a runtime schema validation layer (e.g. `zod`, manual assertions) that rejects invalid values before they are used. Check: non-zero `adapterAddress`, non-empty valid-URL `dataStreamsEndpoint`, positive `intervals[]` divisible by 60, non-zero parseable `gasLimit`.

---

**2. CRE workflow does not validate `adapterAddress != 0x0` before submitting reports**

The CRE workflow reads `adapterAddress` from its config file (`config.production.json` or `config.staging.json`) and uses it as the target for `Multicall3.aggregate3` (in `readRoundConfigs.ts`) and `evmClient.writeReport` (in `writeCloseRounds.ts`). No validation against the zero address before these calls. If `adapterAddress` is the zero address (as the shipped `config.production.json` currently is, pending mainnet deployment), the staticcall to BSC returns `(success=true, data=0x)`, viem's `decodeFunctionResult` throws `AbiDecodingZeroDataError` on empty bytes, and `onCronTrigger` fails silently - the whole cron tick throws. Rounds never close and the operator sees no visible error.

**Impact:** If `adapterAddress` is misconfigured to zero at deployment, the CRE workflow silently halts settlement indefinitely. All rounds stay stuck until the config is fixed and the workflow restarted.

**Recommended:** Add a validation check in `readRoundConfigs.ts` or as an early-exit guard in `onCronTrigger.ts`:

```typescript
if (config.adapterAddress === "0x0000000000000000000000000000000000000000" ||
    !isAddress(config.adapterAddress)) {
  throw new Error(`Invalid adapterAddress in config: ${config.adapterAddress}`);
}
```

---

**3. Init script hardcodes testnet adapter address but accepts mainnet chainid**

`ChainlinkUpDownAdapterInitializeRoundSeries.s.sol:33` hardcodes the adapter address as `0xDB923974731Bdf5C4b1c046522Bf7F99Ee467257` (BSC testnet). Yet `_deployerPrivateKey()` in the same script accepts `block.chainid == 56` (BSC mainnet) and loads `BSC_MAINNET_KEY`. If an operator runs `forge script --chain-id 56` intending mainnet execution, the script signs a transaction with the mainnet private key targeting the testnet address on mainnet - either a no-code address (revert, wasted BNB at mainnet gas prices) or a coincidentally-deployed unrelated contract (unintended behaviour on an unrelated contract).

**Impact:** Operator footgun with real financial consequence. The script as written accepts the mainnet chainid and has no defense against this misconfiguration.

**Recommended:** Either make the adapter address chain-branched (like deployment parameters in `ChainlinkUpDownAdapterDeployment.s.sol`), or add a `require(block.chainid == expectedChainId, ...)` assertion at the top of the script that matches the hardcoded adapter address.

---

**Predict.fun:** Fixed in commit [54b521](https://github.com/PredictDotFun/prediction-market/pull/71/commits/54b521a6a772731ac306ef8e481380ab3f7a73a0), [ba429db](https://github.com/PredictDotFun/prediction-market/pull/71/changes/ba429dbcb9f6edb21da88252d132912ee82f404a), [1209b33](https://github.com/PredictDotFun/prediction-market/commit/1209b338d3520907f4b545d878d045fe2a6a814b), [2371d48](https://github.com/PredictDotFun/prediction-market/pull/71/changes/2371d48af0530187a0458901a3a34493a2c57e8e)

**Cyfrin:** Verified.
