import {Cdm} from "../models/cdm"
import {DynamoDB} from 'aws-sdk';


export class CdmRepo {
    static TABLE_NAME = 'federated-learning-table'
    private dynamodbClient: DynamoDB.DocumentClient

    constructor() {
        this.dynamodbClient = new DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
    }

    async create(model: Cdm) {
        const transactionItems = [{
            Put: {
                Item: model.toItem(),
                TableName: CdmRepo.TABLE_NAME,
                ConditionExpression: "attribute_not_exists(PK)"
            }
        }]
        await this.executeTransactionWrite({
            TransactItems: transactionItems
        })
    }

    executeTransactionWrite(params: any) {
        const transactionRequest = this.dynamodbClient.transactWrite(params)
        let cancellationReasons: string;
        transactionRequest.on('extractError', (response) => {
            try {
                console.log(response.httpResponse.body.toString())
                cancellationReasons = JSON.parse(response.httpResponse.body.toString()).CancellationReasons;
            } catch (err) {
                // suppress this just in case some types of errors aren't JSON parseable
                console.error('Error extracting cancellation error', err);
            }
        });
        return new Promise((resolve, reject) => {
            transactionRequest.send((err, response) => {
                if (err) {
                    // what is the type
                    // err.cancellationReasons = cancellationReasons
                    return reject(err);
                }
                return resolve(response);
            });
        });
    }
}