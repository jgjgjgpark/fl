import {Organization} from "../models/organization";
import {APIGatewayEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {Analysis} from "../models/analysis";
import {AnalysisRepo} from "../repositories/analysis-repo";

async function handler(event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> {
    const organizations: Organization[] = []
    if ("GET" === event.httpMethod) {
        return {
            statusCode: 200,
            body: JSON.stringify({
                data: organizations,
                event: event
            })
        }
    } else if ("POST" === event.httpMethod) {
        // 분석 생성
        let body: { name: string, description: string }
        if (event.body) {
            body = JSON.parse(event.body.toString())
            const analysis = new Analysis(body.name, body.description)
            await new AnalysisRepo().createAnalysis(analysis)
            return {
                statusCode: 200,
                body: JSON.stringify({
                    data: {
                        analysis: analysis
                    }
                })
            }
        } else {
            throw new Error("bad request")
        }
    } else {
        throw new Error("Not Reachable Code")
    }
}

export {handler}