---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: '`swExit::getProcessedRateForTokenId` returns `true` with valid `processedRate`
  for non-existent `tokenId` input'
vuln_class: []
---

# `swExit::getProcessedRateForTokenId` returns `true` with valid `processedRate` for non-existent `tokenId` input

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** `swExit::getProcessedRateForTokenId` returns `true` with valid `processedRate` for non-existent `tokenId` input.

**Impact:** This `public` function can return valid output for invalid input. Currently it only appears to be used by `finalizeWithdrawal` where this behavior does not seem to be further exploitable as that function checks for non-existent tokens before calling `getProcessedRateForTokenId`.

**Proof of Concept:** Add the following PoC to `getProcessedRateForTokenId.test.ts`:
```typescript
  it("Should return false for isProcessed when tokens have been processed but this token doesn't exist", async () => {
    await createWithdrawRequests(Deployer, 5);

    await swEXIT_Deployer.processWithdrawals(4, parseEther("1"));

    // @audit this test fails
    expect(await getProcessedRateForTokenId(0)).eql({
      isProcessed: false,               // @audit returns true
      processedRate: BigNumber.from(0), // @audit returns > 0
    });
  });
```

**Recommended Mitigation:** `swExit::getProcessedRateForTokenId` should `return(false, 0)` when `tokenId` doesn't exist. It appears that the only edge case which is currently unhandled by this function is when `tokenId = 0`.

**Swell:** Fixed in commits [4c8cbfd](https://github.com/SwellNetwork/v3-contracts-lst/commit/4c8cbfde6fdb54385f8bab83c33f90409fd0a412), [262db73](https://github.com/SwellNetwork/v3-contracts-lst/commit/262db7361f543611237e889313b8022a47b77144).

**Cyfrin:**
Verified.
