import {v4} from "uuid";
import {Cdm} from "./cdm";

export class Organization {
    private id: string

    constructor(private name: string, private description: string = '') {
        this.id = v4()
        this.name = name
        this.description = description
    }

    key() {
        return {
            'PK': `ORG#${this.id}`,
            'SK': `ORG#${this.id}`
        }
    }

    toItem() {
        return {
            ...this.key(),
            'type': 'Organization',
            'orgId': this.id,
            'name': this.name,
            'description': this.description
        }
    }
}