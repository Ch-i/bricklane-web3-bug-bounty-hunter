---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-24-cyfrin-linea-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md
tags:
- firm:cyfrin
- report:2024-05-24-cyfrin-linea
title: Associated `finalBlockNumber` for an existing shnarf can be overwritten when
  submitting data using `LineaRollup::submitDataAsCalldata`
vuln_class: []
---

# Associated `finalBlockNumber` for an existing shnarf can be overwritten when submitting data using `LineaRollup::submitDataAsCalldata`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-24-cyfrin-linea.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-24-cyfrin-linea.md)_

---

**Description:** When submitting data using `LineaRollup::submitDataAsCalldata`, if the `computedShnarf` for the current submission turns out to be a shnarf that has already been submitted before, the associated `finalBlockNumber` to this shnarf will be overwritten by the new `submissionData.finalBlockInData`.

The problem is caused because the existing check is comparing if `finalBlockInNumber` associated with the shnarf is the same as the new `submissionData.finalBlockInData`, instead of checking if the shnarf has already been associated with any other `finalBlockNumber`.

**Impact:** Historical data associated with an existing shnarf can be overwritten by the newest shnarf's submission data for blocks which have not yet been finalized.

**Proof of Concept:** Add the PoC to `test/LineaRollup.ts` inside the section `describe("Data submission tests", () => {`:
```typescript
    it.only("Submitting data on a range of blocks where data had already been submitted", async () => {
      let [firstSubmissionData, secondSubmissionData] = generateCallDataSubmission(0, 2);
      const firstParentShnarfData = generateParentShnarfData(0);

      // @audit Assume this is the lastFinalizedBlock, in the sense that any of the
      //        next submissions can't submit data to a block prior to this one
      // @audit The `firstBlockInData` of the next submissions must start at block 550
      firstSubmissionData.finalBlockInData = 549n;
      await expect(
        lineaRollup
          .connect(operator)
          .submitDataAsCalldata(firstParentShnarfData, firstSubmissionData, { gasLimit: 30_000_000 }),
      ).to.not.be.reverted;

      parentSubmissionData = generateParentSubmissionDataForIndex(1);
      const secondParentShnarfData = generateParentShnarfData(1);

      // @audit Submission for block range 550 - 599
      secondSubmissionData.firstBlockInData = 550n;
      secondSubmissionData.finalBlockInData = 599n;
      await expect(
        lineaRollup.connect(operator).submitDataAsCalldata(secondParentShnarfData, secondSubmissionData, {
          gasLimit: 30_000_000,
        }),
      ).to.not.be.reverted;

      let finalBlockNumber = await lineaRollup.shnarfFinalBlockNumbers(secondExpectedShnarf);
      expect(finalBlockNumber == 599n).to.be.true;
      console.log("finalBlockNumber: ", finalBlockNumber);

      // @audit Submission for block range 550 - 649
      //        Instead of continuing from the "lastSubmitedBlock (599)"
      let secondSubmissionOnSameInitialBlockData = Object.assign({}, secondSubmissionData);
      secondSubmissionOnSameInitialBlockData.firstBlockInData = 550n;
      secondSubmissionOnSameInitialBlockData.finalBlockInData = 649n;
      await expect(
        lineaRollup.connect(operator).submitDataAsCalldata(secondParentShnarfData, secondSubmissionOnSameInitialBlockData, {
          gasLimit: 30_000_000,
        }),
      ).to.not.be.reverted;

      finalBlockNumber = await lineaRollup.shnarfFinalBlockNumbers(secondExpectedShnarf);
      expect(finalBlockNumber == 649n).to.be.true;
      console.log("finalBlockNumber: ", finalBlockNumber);

      // @audit Submission for block range 550 - 575
      let thirdSubmissionOnSameInitialBlockData = Object.assign({}, secondSubmissionData);;
      thirdSubmissionOnSameInitialBlockData.firstBlockInData = 550n;
      thirdSubmissionOnSameInitialBlockData.finalBlockInData = 575n;
      await expect(
        lineaRollup.connect(operator).submitDataAsCalldata(secondParentShnarfData, thirdSubmissionOnSameInitialBlockData, {
          gasLimit: 30_000_000,
        }),
      ).to.not.be.reverted;

      finalBlockNumber = await lineaRollup.shnarfFinalBlockNumbers(secondExpectedShnarf);
      expect(finalBlockNumber == 575n).to.be.true;
      console.log("finalBlockNumber: ", finalBlockNumber);

      // @audit Each time a duplicated shnarf was computed the associated
      // `finalBlockNumber` was updated for the new `finalBlockNumber` of the newest submission.
    });
```

Run with: `npx hardhat test --grep "Submitting data on a range of blocks where data had"`

When the test is executed, observe on the console how the `finalBlockNumber` associated with the same shnarf is updated on each of the submissions that generates an existing shnarf which had already been submitted before.

**Recommended Mitigation:** Check if the `computedShnarf` for the current submission has already been associated with a previous `finalBlockInNumber`:

```solidity
function submitDataAsCalldata(
  ...
) external whenTypeAndGeneralNotPaused(PROVING_SYSTEM_PAUSE_TYPE) onlyRole(OPERATOR_ROLE) {
  ...

- if (shnarfFinalBlockNumbers[shnarf] == _submissionData.finalBlockInData) {
-   revert DataAlreadySubmitted(shnarf);
- }

+ if (shnarfFinalBlockNumbers[shnarf] != 0) {
+   revert DataAlreadySubmitted(shnarf);
+ }

  ...
}

```

**Linea:**
Fixed in commit [1816c80](https://github.com/Consensys/zkevm-monorepo/pull/3191/commits/1816c80f8e11528aea48f265bf557b1934023721#diff-408c766d202f05efdde69ebcd815ba16ad10f68249dd353f6359121ab312a9fbR311) merged in [PR3191](https://github.com/Consensys/zkevm-monorepo/pull/3191/files#diff-408c766d202f05efdde69ebcd815ba16ad10f68249dd353f6359121ab312a9fbL311).

**Cyfrin:** Verified.
