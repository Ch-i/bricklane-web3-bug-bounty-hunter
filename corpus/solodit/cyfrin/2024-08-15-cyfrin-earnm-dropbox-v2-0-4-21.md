---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-21
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Use `uint32` for more efficient storage packing when tracking minted and unclaimed
  tier box amounts
vuln_class: []
---

# Use `uint32` for more efficient storage packing when tracking minted and unclaimed tier box amounts

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Firstly change `DropBox` storage like this for more efficient storage slot packing:
* move `vrfHandler` up to the start of the public variables
* change some non-constants to `uint32`
* group all the `uint32` non-constants together just after the `bool` non-constants:
```solidity
contract DropBox is
  IVRFHandlerReceiver,
  DropBoxFractalProtocol,
  ReentrancyGuard,
  OwnableBasic,
  BasicRoyalties,
  ERC721C
{
  using SafeERC20 for IERC20;

  /// @notice - EARNM ERC20 token
  IERC20 internal immutable EARNM;

  /// @notice Public variables
  IVRFHandler public vrfHandler; // VRF Handler to handle the Chainlink VRF requests
  string public _contractURI; // OpenSea Contract-level metadata
  string public _baseTokenURI; // ERC721 Base Token metadata
  address public apiAddress;
  address public feesReceiverAddress;
  uint128 public revealFee = 1 ether;
  uint128 public claimFee = 1 ether;
  bool public isEarnmClaimAllowed;
  bool public isRevealAllowed;

  /// @notice Internal variables
  uint32 internal boxIdCounter = 1; // Counter for the box ids
  uint32 internal remainingBoxesAmount; // Remaining boxes amount to mint
  /// @notice this array stores index: tierId, value: total amount minted
  /// element [0] never used since tierId : [1,6]
  uint32[TIER_IDS_ARRAY_LEN] internal mintedTierAmount;
  uint32[TIER_IDS_ARRAY_LEN] internal unclaimedTierAmount;

  /// @notice Mappings
  mapping(uint256 => Box) internal boxIdToBox; // boxId -> Box
  mapping(bytes32 => OneTimeCode) internal oneTimeCode; // code+address hash -> one-time code data; ensure integrity of
    // one-time code data
  mapping(bytes32 => bool) internal oneTimeCodeUsed; // plain text code -> used (true/false); ensure uniqueness of
    // one-time codes
  mapping(bytes32 => uint256[]) internal oneTimeCodeRandomWords; // code+address hash -> random words
  /// [Chainlink VRF]
  mapping(uint256 => bytes32) internal activeVrfRequests; // vrf request -> code+address hash
  mapping(uint256 => bool) internal fulfilledVrfRequests; // vrf request -> fulfilled

  /// @notice Constants - DropBox
  uint32 internal constant MAX_BOX_AMOUNT_PER_REVEAL = 100;
  uint128 internal constant MAX_MINT_FEE = 1000 ether;
  uint128 internal constant MAX_CLAIM_FEE = 1000 ether;
```

Then change the appropriate types throughout `DropBox.sol`:
```solidity
// function associateOneTimeCodeToAddress,
uint32 remainingBoxesAmountCache = remainingBoxesAmount;

// function claimDropBoxes - see optimized code at end of this issue

// function _assignTierAndMint - see optimized code at end of this issue

// view function return parameters
  function getTotalMaxBoxes() external view returns (uint32 totalMaxBoxes) {
```

And inside `DropBoxFractalProtocol.sol`:
```solidity
// events
event OneTimeCodeAssociated(address indexed claimerAddress, bytes code, uint32 boxAmount);

  /// @notice Constants - Tier max boxes
  uint32 internal immutable TIER_6_MAX_BOXES;
  uint32 internal immutable TIER_5_MAX_BOXES;
  uint32 internal immutable TIER_4_MAX_BOXES;
  uint32 internal immutable TIER_3_MAX_BOXES;
  uint32 internal immutable TIER_2_MAX_BOXES;
  uint32 internal immutable TIER_1_MAX_BOXES;
  uint32 internal immutable TOTAL_MAX_BOXES;

  function _determineTier(
    uint256 randomNumber,
    uint32[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache
```

The test suite also needs some changes:

File: `test/mocks/DropBoxMock.sol`
```solidity
function mock_setUnclaimedTierAmount(uint128 tierId, uint32 amount) public {
function mock_getUnclaimedTierAmount(uint128 tierId) public view returns (uint32) {
function mock_setAllBoxesMinted(uint32 amount) public {

function mock_remainingBoxesAmount() public view returns (uint32) {

  function mock_determineTier(
    uint256 randomNumber,
    uint32[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache

function mock_getMintedTierAmount(uint128 tierId) public view returns (uint32) {
function mock_getMintedTierAmounts() public view returns (uint32[TIER_IDS_ARRAY_LEN] memory) {
function mock_getUnclaimedTierAmounts() public view returns (uint32[TIER_IDS_ARRAY_LEN] memory) {

  function mock_getMaxBoxesPerTier(uint128 tierId) external view returns (uint32 maxBoxesPerTier) {
```

File: `test/DropBox/behaviours/claimDropBox/claimDropBox.t.sol`
```solidity
  function _calculateExpectedClaimAmount(uint256[] memory boxIds)
    internal
    view
    returns (uint256 totalClaimAmount, uint32[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts)

  function _validateClaimedBoxes(
    uint32[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts,

// occurs in 2 few places
    (uint256 expectedAmount, uint32[TIER_IDS_ARRAY_LEN] memory expectedUnclaimedTierAmounts) =
      _calculateExpectedClaimAmount(boxIds);

// near the bottom
    for (uint32 i; i < boxAmount; i++) {
```

File: `test/DropBox/behaviours/earnmInVesting/liability.t.sol`
```solidity
  function _setUnclaimedTierAmounts(uint32[] memory unclaimedAmounts) internal {
  function _calculateExpectedLiability(uint32[] memory unclaimedAmounts) internal view returns (uint256)

    // occurs in a few places
    uint32[] memory unclaimedAmounts = new uint32[](TIER_IDS_LENGTH);
    for (uint32 i = 1; i <= TIER_IDS_LENGTH; i++) {
```

File: `test/DropBox/behaviours/revealDropBox/revealDropBoxes.t.sol`
```solidity
  function _validateMinting(
    address allowedAddress,
    uint32[TIER_IDS_ARRAY_LEN] memory prevMintedTierAmounts,

    for (uint32 i; i < boxAmount; i++) {
```

File: `test/FractalProtocol/FractalProtocol.sol`
```solidity
// occurs many times
    uint32[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache;
```

File: `test/DropBoxFractalProtocolLib.sol`
```solidity
  event OneTimeCodeAssociated(address indexed claimerAddress, bytes code, uint32 boxAmount);
```

After making the above changes everything compiles and all the tests pass when using `gas_limit = "18446744073709551615" # u64::MAX` in `foundry.toml` to raise gas limit for tests which attempt to reveal/claim all boxes.

Using `forge inspect DropBox storage` shows that the regular code used 46 storage slots while the version modified with the above changes uses only 33 storage slots.

Another benefit of this is that the entire arrays `unclaimedTierAmount` and `mintedTierAmount` are now stored in 1 storage slot each as opposed to using 1 storage slot per array element; this means that `claimDropBoxes` and `_assignTierAndMint` can be further simplified and optimized to read and write the arrays once without any conditional tier-based logic:

```solidity
  function claimDropBoxes(uint256[] calldata _boxIds) external payable nonReentrant {
    //
    //  Request Checks
    // ---------------------------------------------------------------------------------------------
    // [Safety check] Only allowed to claim if the isEarnmClaimAllowed variable is true
    // Can be modified by the owner as a safety measure
    if (!(isEarnmClaimAllowed)) revert Unauthorized();

    // [Safety check] Validate that the boxIds array is not empty
    if (_boxIds.length == 0) revert Unauthorized();

    // Require that the user sends a fee of "claimFee" amount
    if (msg.value != claimFee) revert InvalidClaimFee();
    // ---------------------------------------------------------------------------------------------

    // Amount of Earnm tokens to claim
    uint256 amountToClaim;

    // [Gas] Cache unclaimedTierAmount and update cache during the loop then
    // write to storage at the end to prevent multiple update storage writes
    uint32[TIER_IDS_ARRAY_LEN] memory unclaimedTierAmountCache = unclaimedTierAmount;

    //  Earnm Calculation and Safety Checks
    // ---------------------------------------------------------------------------------------------
    // Iterate over box IDs to calculate rewards and validate ownership and uniqueness.
    // - Validate that the sender is the owner of the boxes
    // - Validate that the sender has enough boxes to claim
    // - Validate that the box ids are valid
    // - Validate that the box ids are not duplicated
    // - Calculate the amount of Earnm tokens to claim given the box ids
    for (uint256 i; i < _boxIds.length; i++) {
      // [Safety check] Duplicate values are not allowed
      if (i > 0 && _boxIds[i - 1] >= _boxIds[i]) revert BadRequest();

      // [Safety check] Validate that the box owner is the sender
      if (ownerOf(_boxIds[i]) != msg.sender) revert Unauthorized();

      // Copy the box from the boxes mappings
      Box memory box = boxIdToBox[_boxIds[i]];

      // Increment the amount of Earnm tokens to send to the sender
      amountToClaim += _calculateVestingPeriodPerBox(box.tier, box.blockTs, TIER_IDS_LENGTH);

      // Decrement the unclaimed cached amount for this tier
      --unclaimedTierAmountCache[box.tier];

      // Delete the box from the boxIdToBox mapping
      delete boxIdToBox[_boxIds[i]];

      // Burn the ERC721 token corresponding to the box
      _burn(_boxIds[i]);
    }

    // [Safety check] In case the amount to claim is 0, revert
    if (amountToClaim == 0) revert AmountOfEarnmToClaimIsZero();

    // Update unclaimed tier storage
    unclaimedTierAmount = unclaimedTierAmountCache;

    // ---------------------------------------------------------------------------------------------
    //  Contract Earnm Balance and Safety Checks
    // ---------------------------------------------------------------------------------------------
    // Get the balance of Earnm ERC20 tokens of the contract
    uint256 balance = EARNM.balanceOf(address(this));

    // [Safety check] Validate that the contract has enough Earnm tokens to cover the claim
    if (balance < amountToClaim) revert InsufficientEarnmBalance();
    // ---------------------------------------------------------------------------------------------

    // Emit an event indicating the boxes have been claimed
    emit BoxesClaimed(msg.sender, _boxIds, amountToClaim);

    // Transfer the tokens to the sender
    EARNM.safeTransfer(msg.sender, amountToClaim);
    // ---------------------------------------------------------------------------------------------

    //  Claim Fee Transfer
    // ---------------------------------------------------------------------------------------------
    _sendFee(msg.value);
    // ---------------------------------------------------------------------------------------------
  }

  function _assignTierAndMint(
    uint32 boxAmount,
    uint256[] memory randomNumbers,
    address claimer,
    bytes memory code
  )
    internal
  {
    uint256[] memory boxIdsToEmit = new uint256[](boxAmount);

    // [Gas] Cache mintedTierAmount and update cache during the loop to prevent
    // _determineTier() from re-reading it from storage multiple times
    uint32[TIER_IDS_ARRAY_LEN] memory mintedTierAmountCache = mintedTierAmount;

    // [Gas] Cache unclaimedTierAmount and update cache during the loop then
    // write to storage at the end to prevent multiple update storage writes
    uint32[TIER_IDS_ARRAY_LEN] memory unclaimedTierAmountCache = unclaimedTierAmount;

    // [Gas] cache the current boxId, use cache during the loop then write once
    // at the end; this results in only 1 storage read and 1 storage write for `boxIdCounter`
    uint32 boxIdCounterCache = boxIdCounter;

    // For each box to mint
    for (uint32 i; i < boxAmount; i++) {
      // [Memory] Add the box id to the boxes ids array
      boxIdsToEmit[i] = boxIdCounterCache++;

      // The box seed is directly derived from the random number without any
      // additional values like the box id, the claimer address, or the block timestamp.
      // This is made like this to ensure the tier assignation of the box is purely random
      // and the tier that the box is assigned to, won't change after the randomness is fulfilled.
      // The only way to predict the seed is to know the random number.
      // Random number validation is done in the _fulfillRandomWords function.
      uint256 boxSeed = uint256(keccak256(abi.encode(randomNumbers[i])));

      // Generate a random number between 0 and TOTAL_MAX_BOXES - 1 using the pure random seed
      // Modulo ensures that the random number is within the range of [0, TOTAL_MAX_BOXES) (upper bound exclusive),
      // providing a uniform distribution across the possible range. This ensures that each tier has a
      // probability of being selected proportional to its maximum box count. The randomness is normalized
      // to fit within the predefined total boxes, maintaining the intended probability distribution for each tier.
      //
      // Example with the following setup:
      // _tierMaxBoxes -> [1, 10, 100, 1000, 2000, 6889]
      // _tierNames -> ["Mythical Box", "Legendary Box", "Epic Box", "Rare Box", "Uncommon Box", "Common Box"]
      //
      // The `TOTAL_MAX_BOXES` is the sum of `_tierMaxBoxes`, which is 10_000.
      // The probability distribution is as follows:
      //
      // Mythical Box:   1    / 10_000  chance.
      // Legendary Box:  10   / 10_000  chance.
      // Epic Box:       100  / 10_000  chance.
      // Rare Box:       1000 / 10_000  chance.
      // Uncommon Box:   2000 / 10_000  chance.
      // Common Box:     6889 / 10_000  chance.
      //
      // By using the modulo operation with TOTAL_MAX_BOXES, the random number's probability
      // to land in any given tier is determined by the number of max boxes available for that tier
      uint256 randomNumber = boxSeed % TOTAL_MAX_BOXES;

      // Determine the tier of the box based on the random number
      uint128 tierId = _determineTier(randomNumber, mintedTierAmountCache);

      // [Gas] Adjust the cached amounts for this tier
      ++mintedTierAmountCache[tierId];
      ++unclaimedTierAmountCache[tierId];

      // Save the box to the boxIdToBox mapping
      boxIdToBox[boxIdsToEmit[i]] = Box({ blockTs: uint128(block.timestamp), tier: tierId });

      // Mint the box; explicitly not using `_safeMint` to prevent re-entrancy issues
      _mint(claimer, boxIdsToEmit[i]);
    }

    // Update storage for boxIdCounter
    boxIdCounter = boxIdCounterCache;

    // Update unclaimed & minted tier amounts
    mintedTierAmount = mintedTierAmountCache;
    unclaimedTierAmount = unclaimedTierAmountCache;

    // Emit an event indicating the boxes have been minted
    emit BoxesMinted(claimer, boxIdsToEmit, code);
  }
```

**Mode:**
Fixed in commit [37d258c](https://github.com/Earnft/dropbox-smart-contracts/commit/37d258caa2b6ca07af7f8229951ebf7bc2cd6202).

**Cyfrin:** Verified.
