import { TealContractGenerator } from "./Generator/target/Teal/TealContractGenerator";
import { TealBytesInstanceGenerator } from "./Generator/target/Teal/InstanceExecutionBytes";
import { TealBoxInstanceGenerator } from "./Generator/target/Teal/InstanceExecutionBox";
import { PyTealContractGenerator } from "./Generator/target/Teal/PyTealContractGenerator"

export default {
  generators: {
    teal: {
      DefaultContractGenerator: TealContractGenerator,
      ByteContractGenerator: TealBytesInstanceGenerator,
      BoxContractGenerator: TealBoxInstanceGenerator,
      PTContractGenerator: PyTealContractGenerator
    }
  }
}