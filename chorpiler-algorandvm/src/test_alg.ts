import * as fs from 'fs';
// import chorpiler, { ProcessEncoding, InteractionNet } from '../../chorpiler/lib';
import chorpiler, { ProcessEncoding, InteractionNet } from 'chorpiler';
import algchor from './index'
import path from 'path';

const parser = new chorpiler.Parser();

const contractGenerator = new algchor.generators.teal.PTContractGenerator();
// const contractGenerator = new algchor.generators.teal.DefaultContractGenerator();

// const fileName = "pizza-delivery.bpmn"
// const fileName = "incident-management.bpmn"
// const fileName = "pharmacy.bpmn"
// const fileName = "pharmacy-simplified.bpmn"
// const fileName = "supply-chain.bpmn"
const fileName = "pharmacy-more-simplified.bpmn"
const bpmnXML = fs.readFileSync(path.join(__dirname, "../src/" + fileName));

// parse BPMN file into petri net
parser.fromXML(bpmnXML).then((e: InteractionNet) => {
    // compile to smart contract
    contractGenerator.compile(e)
        .then((gen) => {
            fs.writeFileSync(
                "ProcessExecution.py",
                // "ProcessExecution.teal",
                gen.target,
                { flag: 'w+' }
            );
            console.log("ProcessExecution.teal generated.");
            // log encoding of participants and tasks, 
            // can also be written to a .json file
            console.log(ProcessEncoding.toJSON(gen.encoding));
        })
}).catch((err: any) => console.error(err));