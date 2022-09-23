import {handler} from '../../src/services/repository-create'
describe('table put test', () => {
    it('test', async () => {
        const result = await handler({} as any,{} as any)
        expect(result.body).toBe("'Hello'")
    })
})