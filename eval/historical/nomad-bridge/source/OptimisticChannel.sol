// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

interface IMerkleLib {
    function branchRoot(
        bytes32 leaf,
        bytes32[32] calldata proof,
        uint256 index
    ) external pure returns (bytes32);
}

/// @notice Optimistic message-passing channel. A trusted off-chain Attester
///         publishes merkle roots of message batches; each root becomes
///         spendable after an optimistic challenge window. Once a root is
///         acceptable, any party can submit a merkle proof to mark a
///         message Proven, then call `process` to dispatch it.
contract OptimisticChannel {
    enum MessageStatus {
        None,
        Proven,
        Processed
    }

    address public owner;
    bool private _initialized;

    uint32 public remoteDomain;
    address public attester;
    bytes32 public committedRoot;
    uint256 public challengeSeconds;

    /// @notice Timestamp at which a given merkle root became spendable.
    /// A zero timestamp means "not yet acceptable".
    mapping(bytes32 => uint256) public confirmAt;

    /// @notice State of every message we've seen, keyed by message hash.
    mapping(bytes32 => MessageStatus) public messages;

    IMerkleLib public immutable merkleLib;

    event Process(bytes32 indexed messageHash);
    event RootCommitted(bytes32 indexed root);

    constructor(IMerkleLib _merkleLib) {
        merkleLib = _merkleLib;
    }

    function initialize(
        uint32 _remoteDomain,
        address _attester,
        bytes32 _committedRoot,
        uint256 _challengeSeconds
    ) external {
        require(!_initialized, "already initialized");
        _initialized = true;
        owner = msg.sender;

        remoteDomain = _remoteDomain;
        attester = _attester;
        committedRoot = _committedRoot;
        challengeSeconds = _challengeSeconds;

        // Mark the initial committed root as immediately spendable so the
        // channel can dispatch genesis messages without waiting on a fresh
        // Attester submission.
        confirmAt[_committedRoot] = 1;
    }

    function commit(bytes32 _newRoot, bytes calldata /*_signature*/) external {
        require(msg.sender == attester, "!attester");
        // (signature verification omitted in this minimal version)
        confirmAt[_newRoot] = block.timestamp + challengeSeconds;
        committedRoot = _newRoot;
        emit RootCommitted(_newRoot);
    }

    function isAcceptable(bytes32 _root) public view returns (bool) {
        uint256 _time = confirmAt[_root];
        if (_time == 0) {
            return false;
        }
        return block.timestamp >= _time;
    }

    function prove(
        bytes32 _leaf,
        bytes32[32] calldata _proof,
        uint256 _index
    ) external returns (bool) {
        require(messages[_leaf] == MessageStatus.None, "!new");
        bytes32 _calculatedRoot = merkleLib.branchRoot(_leaf, _proof, _index);
        if (isAcceptable(_calculatedRoot)) {
            messages[_leaf] = MessageStatus.Proven;
            return true;
        }
        return false;
    }

    function process(bytes calldata _message) external returns (bool) {
        bytes32 _messageHash = keccak256(_message);
        require(messages[_messageHash] == MessageStatus.Proven, "!proven");
        messages[_messageHash] = MessageStatus.Processed;
        emit Process(_messageHash);
        // (actual outbound execution / xchain dispatch omitted)
        return true;
    }
}
