import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.27",
  networks: {
    hardhat: {}, // Use the local Hardhat Network
    sepolia: {
      url: `https://eth-sepolia.g.alchemy.com/v2/bZzbYs6LBTEj27hV8Sl_zsuT4e1u6zv6`, // or Infura URL
      accounts: [`0xcc3297f5964b57d54c2d099ead69cd4f0b7ad6745a7a8f2e751bfdb4dab40bd2`], // Your wallet private key
    },
  },
};

export default config;
