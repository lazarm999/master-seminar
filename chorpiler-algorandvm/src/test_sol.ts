import * as fs from 'fs';
import chorpiler, { ProcessEncoding } from 'chorpiler';
import path from 'path';

const parser = new chorpiler.Parser();

const contractGenerator = new chorpiler
    .generators.sol.DefaultContractGenerator();

// const fileName = "pizza-delivery.bpmn"
// const fileName = "incident-management.bpmn"
// const fileName = "pharmacy.bpmn"
// const fileName = "pharmacy-simplified.bpmn"
// const fileName = "supply-chain.bpmn"
const fileName = "pharmacy-more-simplified.bpmn"

const bpmnXML = fs.readFileSync(path.join(__dirname, "../src/" + fileName));

parser.fromXML(bpmnXML).then((e) => {
    // compile to smart contract
    contractGenerator.compile(e)
        .then((gen) => {
            fs.writeFileSync(
                "Process.sol",
                gen.target,
                { flag: 'w+' }
            );
            console.log("Process.sol generated.");
            // log encoding of participants and tasks, 
            // can also be written to a .json file
            console.log(ProcessEncoding.toJSON(gen.encoding));
        })
}).catch((err: any) => console.error(err));