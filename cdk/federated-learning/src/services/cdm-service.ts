import {APIGatewayEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {DynamoDB} from 'aws-sdk'

const dbClient = new DynamoDB.DocumentClient()

async function handler(event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> {
    const data:any = await query();
    if ("GET" === event.httpMethod) {
        return {
            statusCode: 200,
            body: JSON.stringify({
                data: data
            })
        }
    } else {
        throw new Error("Not Reachable Code")
    }
}

async function query() {
    return new Promise((resolve, reject) => {
        dbClient.query({
            TableName: "federated-learning-table",
            IndexName: "globalIndex2",
            KeyConditionExpression: "GSI1PK = :value",
            ExpressionAttributeValues: {
                ":value": "ALL_CDM"
            },
            ProjectionExpression: "cdmId, description"
        }, (err, data) => {
            if (err) {
                return reject(err)
            }
            return resolve(data)
        })
    })
}

async function query1() {
    return new Promise((resolve, reject) => {
        dbClient.query({
            TableName: "federated-learning-table",
            KeyConditionExpression: "PK = :value",
            ExpressionAttributeValues: {
                ":value": "ORG#1"
            }
        }, (err, data) => {
            if (err) {
                return reject(err)
            }
            return resolve(data)
        })
    })
}

export {handler}