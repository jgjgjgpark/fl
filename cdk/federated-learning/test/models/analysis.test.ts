import {Analysis} from "../../src/models/analysis";

describe('Analysis', ()=>{
    it('test', ()=>{
        const analysis = new Analysis("test", "test")
        console.log(analysis.toItem())
        // const names = key.split('/')
        // expect(names[0]).toBe('16a22842-39cf-4fdb-a729-2a96eb43810b')

    })
})