import {Organization} from "../../src/models/organization";

describe('Organization', ()=>{
    it('test', ()=>{
        const key = '16a22842-39cf-4fdb-a729-2a96eb43810b/round_1/input/input.zip'
        const names = key.split('/')
        expect(names[0]).toBe('16a22842-39cf-4fdb-a729-2a96eb43810b')

    })
})