// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract ProcessExecution {
    uint public tokenState = 1;
    address[5] public participants;

    constructor(address[5] memory _participants) {
        participants = _participants;
    }

    function getTokenState() public view returns (uint) {
        return tokenState;
    }

    function resetTokenState() public returns (uint) {
        tokenState = 1;
        return tokenState;
    }

    function enact(uint id) external returns (uint) {
        uint _tokenState = tokenState;

        while (true) {
            if (
                id == 0 &&
                (_tokenState & 1 == 1) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(1);
                _tokenState |= 2;
                break;
            }
            if (
                id == 1 &&
                (_tokenState & 2 == 2) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(2);
                _tokenState |= 4;
                break;
            }
            if (
                id == 2 &&
                (_tokenState & 4 == 4) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(4);
                _tokenState |= 8;
                break;
            }
            if (
                id == 3 &&
                (_tokenState & 8 == 8) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(8);
                _tokenState |= 16;
                break;
            }
            if (
                id == 4 &&
                (_tokenState & 16 == 16) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(16);
                _tokenState |= 32;
                break;
            }
            if (
                id == 5 &&
                (_tokenState & 32 == 32) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(32);
                _tokenState |= 64;
                break;
            }
            if (
                id == 6 &&
                (_tokenState & 64 == 64) &&
                msg.sender == participants[0]
            ) {
                _tokenState &= ~uint(64);
                _tokenState |= 0;
                break;
            }
        }

        tokenState = _tokenState;
        return tokenState;
    }
}
