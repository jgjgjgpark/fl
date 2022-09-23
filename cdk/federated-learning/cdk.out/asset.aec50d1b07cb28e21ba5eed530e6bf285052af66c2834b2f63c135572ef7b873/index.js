"use strict";
var __defProp = Object.defineProperty;
var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};
var __copyProps = (to, from, except, desc) => {
  if (from && typeof from === "object" || typeof from === "function") {
    for (let key of __getOwnPropNames(from))
      if (!__hasOwnProp.call(to, key) && key !== except)
        __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
  }
  return to;
};
var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

// src/services/s3-event-listener.ts
var s3_event_listener_exports = {};
__export(s3_event_listener_exports, {
  handler: () => handler
});
module.exports = __toCommonJS(s3_event_listener_exports);
function getAnalysisIdAndFileName(event) {
  const fileName = event.Records[0].s3.object.key;
  console.log(`fileName: ${fileName}`);
  const names = fileName.split("/");
  return names[0], names[names.length - 1];
}
function isInput(fileName) {
  return fileName == "input.zip";
}
function isResult(fileName) {
  return fileName == "result.zip";
}
function executeAnalysis() {
}
function updateState() {
}
async function handler(event, context) {
  let message = "";
  console.log(event);
  const [analysisId, fileName] = getAnalysisIdAndFileName(event);
  console.log("analysisId: ${analysisId}");
  if (isInput(fileName)) {
    executeAnalysis();
    message = "execute analysis";
  } else if (isResult(fileName)) {
    updateState();
    message = "organization#1 round#1 execution completed successfully";
  } else {
    throw new Error("Unreachable Code");
  }
  return {
    body: JSON.stringify({ message }),
    statusCode: 200
  };
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  handler
});
