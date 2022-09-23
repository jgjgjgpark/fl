import {GetObjectCommand, PutObjectCommand, S3Client} from "@aws-sdk/client-s3"
import {APIGatewayEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {getSignedUrl} from "@aws-sdk/s3-request-presigner";

function s3Client() {
    const region = "ap-northeast-2"
    return new S3Client({region})
}

async function handler(event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> {
    if ("GET" === event.httpMethod) {
        const analysisId = event.pathParameters?.analysisId
        const round = event.queryStringParameters?.round
        // const analysisId = 'test'
        let bucketParams = {
            Bucket: `federated-learning-bucket`,
            Key: `${analysisId}/round_${round}/input/input.zip`,
            // Body: "BODY",
            // ContentType: "application/octet-stream"
        };
        const command = new PutObjectCommand(bucketParams)
        // const command = new GetObjectCommand(bucketParams)
        const signedUrl = await getSignedUrl(s3Client(), command, {
            expiresIn: 3600
        })
        return {
            statusCode: 200,
            body: JSON.stringify({
                data: signedUrl
            })
        }
    } else {
        throw new Error("Not Reachable Code")
    }
}

export {handler}