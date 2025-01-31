//SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract ProcessExecution {
  uint public tokenState = 1;
  address[5] public participants;

  constructor(address[5] memory _participants) {
    participants = _participants;
  }

  function enact(uint id) external {
    uint _tokenState = tokenState;

    while(true) {
        if (msg.sender == participants[3] && 0 == id && (_tokenState & 1 == 1)) {
          _tokenState &= ~uint(1);
          _tokenState |= 2;
          break;
        }
        if (msg.sender == participants[4] && 1 == id && (_tokenState & 4 == 4)) {
          _tokenState &= ~uint(4);
          _tokenState |= 0;
          break;
        }
        if (msg.sender == participants[4] && 2 == id && (_tokenState & 2 == 2)) {
          _tokenState &= ~uint(2);
          _tokenState |= 8;
          break;
        }
        if (msg.sender == participants[0] && 3 == id && (_tokenState & 16 == 16)) {
          _tokenState &= ~uint(16);
          _tokenState |= 1;
          break;
        }
        if (msg.sender == participants[1] && 4 == id && (_tokenState & 32 == 32)) {
          _tokenState &= ~uint(32);
          _tokenState |= 64;
          break;
        }
        if (msg.sender == participants[4] && 5 == id && (_tokenState & 64 == 64)) {
          _tokenState &= ~uint(64);
          _tokenState |= 4;
          break;
        }
        if (msg.sender == participants[2] && 6 == id && (_tokenState & 8 == 8)) {
          _tokenState &= ~uint(8);
          _tokenState |= 32;
          break;
        }
      return;
    }


    tokenState = _tokenState;
  }
}