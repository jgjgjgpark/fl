import {Organization} from "../models/organization";
import {APIGatewayEvent, APIGatewayProxyResult, Context} from "aws-lambda";
import {OrganizationRepo} from "../repositories/organization-repo";

async function handler(event: APIGatewayEvent, context: Context): Promise<APIGatewayProxyResult> {
    const organizations: Organization[] = []
    organizations.push(new Organization("severance"))
    organizations.push(new Organization("samsung hospital"))
    organizations.push(new Organization("ajou hospital"))
    organizations.push(new Organization("gil hospital"))
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
            const organization = new Organization(body.name, body.description)
            await new OrganizationRepo().create(organization)
            return {
                statusCode: 200,
                body: JSON.stringify({
                    data: organization
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