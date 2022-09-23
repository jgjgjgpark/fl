import {v4} from "uuid";

export class Cdm {
    private readonly id: string

    constructor(private orgId: string, private readonly name: string, private readonly description: string) {
        this.orgId = orgId
        this.id = v4()
        this.name = name
        this.description = description
    }

    key() {
        return {
            'PK': `ORG#${this.orgId}`,
            'SK': `CDM#${this.id}`
        }
    }

    toItem() {
        return {
            ...this.key(),
            ...this.gsi1(),
            'type': 'Cdm',
            'cdmId': this.id,
            'orgId': this.orgId,
            'name': this.name,
            'description': this.description
        }
    }

    gsi1() {
        return {
            'GSI1PK': 'ALL_CDM',
            'GSI1SK': `CDM#${this.id}`,
        }
    }
}