import { ethers } from "hardhat";
import { ethers as otherEthers } from "ethers";
import { HardhatEthersSigner } from "@nomicfoundation/hardhat-ethers/signers";

let accounts = []

function getRandomInt(max: number) {
    return Math.floor(Math.random() * max);
}

function createAccounts(n: number) {
    // Generate a random wallet
    accounts = []
    for (let i = 1; i <= n; i++) {
        const acc = ethers.Wallet.createRandom()
        accounts.push(acc.address);
        console.log("Address:", acc.address); // Public address
        console.log("Private Key:", acc.privateKey); // Private key
    }
    return accounts;
}

async function deployContract(contractName: string, ...args: any[]) {
    const processFactory = await ethers.getContractFactory(contractName);
    return await processFactory.deploy(...args);
}

async function deployProcessExecutionSimpleContract(participantsNum: number) {
    //     const signers = await ethers.getSigners();
    //     const addresses = signers?.slice(0, participantsNum)?.map((s) => s.address);
    const addresses = createAccounts(4)
    addresses.unshift("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62")
    return deployContract("ProcessExecutionSimpleContract", addresses);
}

async function calculateTotalBalance(signers: HardhatEthersSigner[]): Promise<bigint> {
    const provider = ethers.provider;
    let sum = 0n;
    for (let i = 0; i < signers.length; i++) {
        const s = signers[i];
        sum += await provider.getBalance(s.address)
    }
    return sum;
}

async function localTestProcessExecution(contract: any) {
    const participantsOrder = [0, 1, 2, 3, 4, 2, 2]
    const signers = await ethers.getSigners();
    const startSum = await calculateTotalBalance(signers);
    let sumFromTransactions: bigint = 0n;
    for (let i = 0; i < participantsOrder.length; i++) {
        const enactTx = await contract.connect(signers[participantsOrder[i]]).enact(i);
        const txData = await enactTx.wait();
        console.log("txData", txData);
        console.log(`Gas Used: ${txData?.gasUsed?.toString()}`);
        console.log(`Gas price: ${txData?.gasPrice?.toString()}`);
        sumFromTransactions += BigInt(txData.gasUsed) * BigInt(txData.gasPrice);
    }
    const endSum = await calculateTotalBalance(signers);
    console.log("Total gas spent: ", startSum - endSum);
    console.log("Should be same:  ", sumFromTransactions);
}

async function sepoliaTestProcessExecution(contract: any) {
    const provider = ethers.provider;
    const startBalance = await provider.getBalance("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62");
    const signer = new ethers.Wallet("0xcc3297f5964b57d54c2d099ead69cd4f0b7ad6745a7a8f2e751bfdb4dab40bd2", provider);
    let sumFromTransactions: bigint = 0n;
    const contractStartTime = Date.now();
    const transactionTimes = [];
    for (let i = 1; i < 7; i++) {
        const transactionStartTime = Date.now();
        const enactTx = await contract.connect(signer).enact(i);
        const txData = await enactTx.wait();
        const transactionEndTime = Date.now();
        // console.log("txData", txData);
        console.log(`Gas Used: ${txData?.gasUsed?.toString()}`);
        console.log(`Gas price: ${txData?.gasPrice?.toString()}`);
        sumFromTransactions += BigInt(txData.gasUsed) * BigInt(txData.gasPrice);
        transactionTimes.push(transactionEndTime - transactionStartTime)
    }
    const contractEndTime = Date.now();
    const endBalance = await provider.getBalance("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62")
    console.log("Total gas spent: ", startBalance - endBalance);
    console.log("Should be same:  ", sumFromTransactions);
    console.log("Transaction times: ", transactionTimes);
    console.log("Contract total time: ", contractEndTime - contractStartTime)
}

async function sendETH(amount: number) {
    // const amount = ethers.utils.parseEther("0.1"); // Converts Ether to wei

    const receiverAddress = "0xf533071F0093Ed3984A07Ad8252c7a61aaC374b1"
    const sender = new ethers.Wallet("0xcc3297f5964b57d54c2d099ead69cd4f0b7ad6745a7a8f2e751bfdb4dab40bd2", ethers.provider);
    // Create and send the transaction

    const transactionStartTime = Date.now();
    const tx = await sender.sendTransaction({
        to: receiverAddress,
        value: amount,
    });
    const txData = await tx.wait();
    const transactionEndTime = Date.now();

    console.log("Transaction time: " + (transactionEndTime - transactionStartTime))
    console.log(`Gas Used: ${txData?.gasUsed?.toString()}`);
    console.log(`Gas price: ${txData?.gasPrice?.toString()}`);
}

async function main() {
    const provider = ethers.provider;
    let startBalance = await provider.getBalance("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62");
    console.log(startBalance)

    for (let i = 0; i < 1; i++) {
        await sendETH(100000);
    }

    const endBalance = await provider.getBalance("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62");
    console.log(endBalance)

    // const contract = await deployProcessExecutionSimpleContract(5);
    // console.log(contract)

    // const provider = ethers.provider;
    // const startBalance = await provider.getBalance("0xf3e6B3B0BBd8437e3b068E4f23F5d52fA9cdAb62");
    // console.log(startBalance)

    // old 0xB33cfaB15641f42e63E82724AcB5F6b827f33247
    // const contractAddress = "0xFE30100d9e4cee56aCB13572A05744dDB92aC569"
    // vidi ako u liniji ispod treba da promenisi iz ProcessExecution u ProcessExecutionSimpleContract
    // const processExecutionContract = await ethers.getContractAt("ProcessExecution", contractAddress);
    // await sepoliaTestProcessExecution(processExecutionContract);

    // const simpleContract = await deployContractWithFactory("SimpleContract", 1)
    // console.log("Contract Deployed to Address:", simpleContract);

    // const contractAddress = "0x9e31A16632d84487B1a2042Ae337f14381a8A6c4"
    // const contractAddress = "0x66E9E5852B8ffEBA64a770f6E20D25eeEA5Df572"
    // const simpleContract = await ethers.getContractAt("SimpleContract", contractAddress);
    // const tx = await simpleContract.set(42); // Set value
    // console.log(`tx: ${tx.data}`);
    // const oldValue = await simpleContract.get(); // Get the stored value
    // console.log(`Stored value is: ${oldValue}`);

    // Display gas and transaction details
    // console.log(`Gas Used: ${receipt?.gasUsed?.toString()}`);
    // console.log(`Receipt: ${receipt?.gasPrice?.toString()}`);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
