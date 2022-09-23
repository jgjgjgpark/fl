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

// src/services/cdm-service.ts
var cdm_service_exports = {};
__export(cdm_service_exports, {
  handler: () => handler
});
module.exports = __toCommonJS(cdm_service_exports);
var import_aws_sdk = require("aws-sdk");
var dbClient = new import_aws_sdk.DynamoDB.DocumentClient();
async function handler(event, context) {
  const data = await query();
  if (event.httpMethod === "GET") {
    return {
      statusCode: 200,
      body: JSON.stringify({
        data: data.Items,
        event
      })
    };
  } else {
    throw new Error("Not Reachable Code");
  }
}
async function query() {
  return new Promise((resolve, reject) => {
    dbClient.query({
      TableName: "federated-learning-table",
      IndexName: "globalIndex2",
      KeyConditionExpression: "GSI1PK = :value",
      ExpressionAttributeValues: {
        ":value": "ALL_CDM"
      },
      ProjectionExpression: "cdmId, description"
    }, (err, data) => {
      if (err) {
        return reject(err);
      }
      return resolve(data);
    });
  });
}
// Annotate the CommonJS export names for ESM import in node:
0 && (module.exports = {
  handler
});
