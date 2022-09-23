import {Organization} from "../models/organization";
import {APIGatewayEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {GetObjectCommand, S3Client} from "@aws-sdk/client-s3";
import {getSignedUrl} from "@aws-sdk/s3-request-presigner";
function s3Client() {
    const region = "ap-northeast-2"
    return new S3Client({region})
}
async function handler(event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> {
    if ("PUT" === event.httpMethod) {
        const analysisId = event.pathParameters?.analysisId
        const round = event.pathParameters?.round
        let bucketParams = {
            Bucket: `federated-learning-bucket`,
            Key: `${analysisId}/round_${round}/input/input.zip`,
            // Body: "BODY",
            // ContentType: "application/octet-stream"
        };
        const command = new GetObjectCommand(bucketParams)
        const signedUrl = await getSignedUrl(s3Client(), command, {
            expiresIn: 36000
        })
        return {
            statusCode: 200,
            body: JSON.stringify({
                presignedGetUrl: signedUrl,
                round
            })
        }
    } else {
        throw new Error("Not Reachable Code")
    }
}

export {handler}