// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleContract {
    uint256 private storedData;

    constructor(uint256 defaultValue) {
        storedData = defaultValue;
    }

    // Set the value
    function set(uint256 x) public returns (uint256) {
        storedData = x;
        return 200;
    }

    // Get the stored value
    function get() public view returns (uint256) {
        return storedData;
    }
}
