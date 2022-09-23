import {DynamoDB} from 'aws-sdk'
import {APIGatewayProxyEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {v4} from "uuid";


const dbClient = new DynamoDB.DocumentClient()

async function handler(event: APIGatewayProxyEvent, context: Context): Promise<APIGatewayProxyResult> {
    const result: APIGatewayProxyResult = {
        statusCode: 200,
        body: 'HElo'
    }
    const item = typeof event.body == 'object' ? event.body : JSON.parse(event.body)
    item.spaceId = v4()
    try {
        const queryResponse = await dbClient.scan({
            TableName: 'FederatedLearningTable'
        }).promise()
        result.body = JSON.stringify(queryResponse)
    } catch (error) {
        result.body = error.message
    }
    return result;
}

export {handler}