import {Context, S3Event} from "aws-lambda";

function getAnalysisIdAndFileName(event: S3Event) {
    const fileName = event.Records[0].s3.object.key
    console.log(`fileName: ${fileName}`)
    const names = fileName.split('/')
    return [names[0], names[names.length - 1]]
}

function isInput(fileName: string) {
    return 'input.zip' == fileName
}

function isResult(fileName: string) {
    return 'result.zip' == fileName;
}

/**
 * 1. get organizations involved in analysis
 * 2. invoke organizations' analysis
 * 3. update analysis status --> analysis roundXX running
 */
function executeAnalysis() {

}

/**
 * update dynamo db
 */
function updateState() {

}

async function handler(event: S3Event, context: Context) {
    let message = ''
    console.log(event)
    const [analysisId, fileName] = getAnalysisIdAndFileName(event)
    console.log("analysisId: ${analysisId}")
    if (isInput(fileName)) {
        executeAnalysis()
        message = 'execute analysis'
    } else if (isResult(fileName)) {
        updateState()
        message = 'organization#1 round#1 execution completed successfully'
    } else {
        throw new Error("Unreachable Code")
    }
    return {
        body: JSON.stringify({message}),
        statusCode: 200
    }
}

export {handler}