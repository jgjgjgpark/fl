import {handler} from "../../src/services/organization-service";

function getAnalysisIdAndFileName() {
    const fileName = '16a22842-39cf-4fdb-a729-2a96eb43810b/round_1/input/input.zip'
    console.log(`fileName: ${fileName}`)
    const names = fileName.split('/')
    return [names[0], names[names.length - 1]]
}

describe('Organization', () => {
    it('test', () => {
        const key = '16a22842-39cf-4fdb-a729-2a96eb43810b/round_1/input/input.zip'
        const names = key.split('/')
        expect(names[names.length - 1]).toBe('input.zip')

    })
    it('test1', () => {
        const [analysisId, fileName] = getAnalysisIdAndFileName()
        expect(analysisId).toBe('16a22842-39cf-4fdb-a729-2a96eb43810b')
        expect(fileName).toBe('input.zip')
    })
    it('undefined or .. test', () => {
        let a: string | undefined
        let k = 2
        if (k == 1) {
            a = undefined
        } else {
            a = "Test"
        }
        console.log(a?.length)
    })
})