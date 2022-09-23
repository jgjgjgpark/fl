import {v4} from "uuid";


export class Analysis {
    private analysisId: string
    private status: string

    constructor(private name: string, private description: string, private cdms: string[],  private createdAt = new Date()) {
        this.analysisId = v4()
        this.name = name
        this.description = description
        this.cdms = cdms
        this.createdAt = createdAt
        this.status = "created"
    }

    execute() {

    }

    key() {
        return {
            'PK': `ANALYSIS#${this.analysisId}`,
            'SK': `ANALYSIS#${this.analysisId}`
        }
    }

    toItem() {
        return {
            ...this.key(),
            'type': 'Analysis',
            'analysisId': this.analysisId,
            'name': this.name,
            'description': this.description,
            'cdms': this.cdms,
            'status': this.status,
            'createdAt': this.createdAt.toISOString()
        }
    }
}