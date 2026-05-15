// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

/// @notice ETH liquidity pool that pays a share of accrued protocol fees
///         pro-rata to depositors. Users deposit ETH, harvest accrued
///         rewards on demand, and withdraw their principal at any time.
contract LiquidityPool {
    address public owner;
    uint256 public totalDeposits;
    uint256 public rewardPerEthScaled; // accumulator (1e18 fixed point)

    mapping(address => uint256) public balances;
    mapping(address => uint256) public rewardDebt;

    event Deposited(address indexed user, uint256 amount);
    event Withdrew(address indexed user, uint256 amount);
    event Harvested(address indexed user, uint256 reward);
    event RewardAdded(uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "!owner");
        _;
    }

    function deposit() external payable {
        require(msg.value > 0, "zero deposit");

        // Settle any pending reward for this depositor before changing balance.
        uint256 pending = _pending(msg.sender);
        if (pending > 0) {
            (bool ok, ) = msg.sender.call{value: pending}("");
            require(ok, "reward send failed");
            emit Harvested(msg.sender, pending);
        }

        balances[msg.sender] += msg.value;
        totalDeposits += msg.value;
        rewardDebt[msg.sender] = (balances[msg.sender] * rewardPerEthScaled) / 1e18;

        emit Deposited(msg.sender, msg.value);
    }

    function harvest() external {
        uint256 pending = _pending(msg.sender);
        require(pending > 0, "nothing to claim");

        // Update accounting before transfer.
        rewardDebt[msg.sender] = (balances[msg.sender] * rewardPerEthScaled) / 1e18;

        (bool ok, ) = msg.sender.call{value: pending}("");
        require(ok, "reward send failed");
        emit Harvested(msg.sender, pending);
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient balance");

        uint256 pending = _pending(msg.sender);
        uint256 payout = amount + pending;

        (bool ok, ) = msg.sender.call{value: payout}("");
        require(ok, "withdraw send failed");

        balances[msg.sender] -= amount;
        totalDeposits -= amount;
        rewardDebt[msg.sender] = (balances[msg.sender] * rewardPerEthScaled) / 1e18;

        emit Withdrew(msg.sender, amount);
        if (pending > 0) emit Harvested(msg.sender, pending);
    }

    /// @notice Owner credits new reward ETH to depositors, distributed pro-rata.
    function addReward() external payable onlyOwner {
        require(totalDeposits > 0, "no depositors");
        require(msg.value > 0, "zero reward");
        rewardPerEthScaled += (msg.value * 1e18) / totalDeposits;
        emit RewardAdded(msg.value);
    }

    function _pending(address user) internal view returns (uint256) {
        uint256 accumulated = (balances[user] * rewardPerEthScaled) / 1e18;
        if (accumulated <= rewardDebt[user]) return 0;
        return accumulated - rewardDebt[user];
    }

    receive() external payable {
        // Allow protocol-level inflows (fees, rebates) to accrue as a "donation"
        // to the rewardPerEthScaled accumulator at the owner's discretion.
    }
}
