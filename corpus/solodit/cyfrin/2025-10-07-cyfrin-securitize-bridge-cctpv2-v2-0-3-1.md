---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Fail fast without doing unnecessary work
vuln_class: []
---

# Fail fast without doing unnecessary work

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** If a transaction is going to revert, then revert as fast as possible without doing unnecessary work. Strategies to achieve this include:
* perform all input-related validation first
* read only enough storage or make enough external calls to perform the next validation step

For example in `SecuritizeBridge::bridgeDSTokens`:
```solidity
    function bridgeDSTokens(uint16 targetChain, uint256 value) external override payable whenNotPaused {
        // @audit why do all this work...
        uint256 cost = quoteBridge(targetChain);
        require(msg.value >= cost, "Transaction value should be equal or greater than quoteBridge response");
        require(dsToken.balanceOf(_msgSender()) >= value, "Not enough balance in source chain to bridge");
        address targetAddress = bridgeAddresses[targetChain];
        require(bridgeAddresses[targetChain] != address(0), "No bridge address available");

        IDSRegistryService registryService = IDSRegistryService(dsServiceConsumer.getDSService(dsServiceConsumer.REGISTRY_SERVICE()));
        require(registryService.isWallet(_msgSender()), "Investor not registered");

        // @audit ...if txn will revert here due to invalid input?
        require(value > 0, "DSToken value must be greater than 0");
```

And in `USDCBridgeV2::sendUSDCCrossChainDeposit`
```solidity
    function sendUSDCCrossChainDeposit(
        uint16 _targetChain,
        address _recipient,
        uint256 _amount
    ) external override whenNotPaused nonReentrant onlyRole(BRIDGE_CALLER) {
        uint256 deliveryCost = quoteBridge(_targetChain);
        // @audit why perform this storage read...
        address targetBridge = bridgeAddresses[_targetChain];
        // @audit ...if this check will just revert? Perform this check immediately
        // after `uint256 deliveryCost = quoteBridge(_targetChain);`
        if (address(this).balance < deliveryCost) {
            revert InsufficientContractBalance();
        }
        // @audit why perform this check here?
        if (IERC20(USDC).balanceOf(_msgSender()) < _amount) {
            revert NotEnoughBalance();
        }
        // @audit if it is going to revert from this? Perform this check immediately
        // after ` address targetBridge = bridgeAddresses[_targetChain];`
        if (targetBridge == address(0)) {
            revert BridgeAddressUndefined();
        }
```

**Securitize:** Fixed in commit [2ad89cf](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/2ad89cf65ea61c999f140fa6754fb1077a3674b1).

**Cyfrin:** Verified.
