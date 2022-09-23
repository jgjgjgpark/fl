import {DynamoDB} from 'aws-sdk'
import {APIGatewayProxyEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {v4} from "uuid";


const dbClient = new DynamoDB.DocumentClient()

async function handler(event: APIGatewayProxyEvent, context: Context): Promise<APIGatewayProxyResult> {
    const result: APIGatewayProxyResult = {
        statusCode: 200,
        body: 'Hello'
    }
    const item = {
        PK: v4()
    }
    try {
        await dbClient.put({
            TableName: 'federated-learning-table',
            Item: item
        }).promise()
    } catch (error) {
        result.body = error.message
    }
    return result;
}

export {handler}