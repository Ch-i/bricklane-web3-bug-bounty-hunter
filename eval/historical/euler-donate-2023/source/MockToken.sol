// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

/// @notice Minimal ERC20 stub used by CreditMarket. Just enough surface for
///         the lending logic; no allowances, no events, no decimals tricks.
contract MockToken {
    string public constant name = "Underlying";
    string public constant symbol = "U";
    uint8 public constant decimals = 18;

    mapping(address => uint256) public balanceOf;
    uint256 public totalSupply;

    function mint(address to, uint256 amount) external {
        balanceOf[to] += amount;
        totalSupply += amount;
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        unchecked {
            balanceOf[msg.sender] -= amount;
        }
        balanceOf[to] += amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(balanceOf[from] >= amount, "insufficient");
        unchecked {
            balanceOf[from] -= amount;
        }
        balanceOf[to] += amount;
        return true;
    }
}
