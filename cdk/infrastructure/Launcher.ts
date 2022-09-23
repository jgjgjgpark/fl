import {App} from "aws-cdk-lib";
import {FLStack} from "./FLStack";

const app = new App()
new FLStack(app, 'Federated-Learning', {
    stackName: 'FederatedLearning'
})