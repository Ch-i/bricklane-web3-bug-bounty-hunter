---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Protocol Fee Recipient Updates Are Not Enforced On Old EulerSwap Instances
vuln_class: []
---

# Protocol Fee Recipient Updates Are Not Enforced On Old EulerSwap Instances

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** The `protocolFeeRecipient` value is stored in the parameters of each `EulerSwap` instance at the time of its deployment. When the [`ProtocolFee::setProtocolFeeRecipient`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/utils/ProtocolFee.sol#L21-L23) function in the `ProtocolFee` contract is called to update the `protocolFeeRecipient`, the change only affects new instances of `EulerSwap` deployed after the update. Existing `EulerSwap` instances retain the old `protocolFeeRecipient` value since it is embedded in their parameters during deployment and is not dynamically referenced.

**Impact:** This creates a discrepancy where older `EulerSwap` instances continue to send protocol fees to the outdated recipient address, potentially leading to financial losses or mismanagement of funds. It also introduces operational complexity, as the protocol owner must manually update or redeploy affected `EulerSwap` instances to align them with the new recipient address.

**Proof of Concept:** Add the following test to the `HookFees.t.sol` file:
```solidity
function test_protocolFeeRecipientChange() public {
	// Define two protocol fee recipients
	address recipient1 = makeAddr("recipient1");
	address recipient2 = makeAddr("recipient2");

	// Set initial protocol fee and recipient in factory
	uint256 protocolFee = 0.1e18; // 10% of LP fee
	eulerSwapFactory.setProtocolFee(protocolFee);
	eulerSwapFactory.setProtocolFeeRecipient(recipient1);

	// Deploy pool1 with recipient1
	EulerSwap pool1 = createEulerSwapHookFull(
		60e18,
		60e18,
		0.001e18,
		1e18,
		1e18,
		0.4e18,
		0.85e18,
		protocolFee,
		recipient1
	);

	// Verify pool1's protocolFeeRecipient
	IEulerSwap.Params memory params1 = pool1.getParams();
	assertEq(params1.protocolFeeRecipient, recipient1);

	// Perform a swap in pool1
	uint256 amountIn = 1e18;
	assetTST.mint(anyone, amountIn);
	vm.startPrank(anyone);
	assetTST.approve(address(minimalRouter), amountIn);
	bool zeroForOne = address(assetTST) < address(assetTST2);
	minimalRouter.swap(pool1.poolKey(), zeroForOne, amountIn, 0, "");
	vm.stopPrank();

	// Check that fees were sent to recipient1
	uint256 feeCollected1 = assetTST.balanceOf(recipient1);
	assertGt(feeCollected1, 0);
	assertEq(assetTST.balanceOf(recipient2), 0);

	// Change protocolFeeRecipient to recipient2 in factory
	eulerSwapFactory.setProtocolFeeRecipient(recipient2);

	// Perform another swap in pool1
	assetTST.mint(anyone, amountIn);
	vm.startPrank(anyone);
	assetTST.approve(address(minimalRouter), amountIn);
	minimalRouter.swap(pool1.poolKey(), zeroForOne, amountIn, 0, "");
	vm.stopPrank();

	// Check that additional fees were sent to recipient1, not recipient2
	uint256 newFeeCollected1 = assetTST.balanceOf(recipient1);
	assertGt(newFeeCollected1, feeCollected1); // recipient1 received more fees
	assertEq(assetTST.balanceOf(recipient2), 0); // recipient2's balance unchanged
}
```

**Recommended Mitigation:** Refactor the `EulerSwap` contract to reference the `protocolFeeRecipient` dynamically from the `EulerSwapFactory` contract instead of storing it in the deployment parameters. This ensures that any updates to the `protocolFeeRecipient` are immediately reflected across all `EulerSwap` instances, both old and new.

**Euler:** Acknowledged.
