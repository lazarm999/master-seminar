import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("SimpleContract", (m) => {
    const contract = m.contract("SimpleContract", [1]);

    m.call(contract, "set", [2]);

    return { contract };
});