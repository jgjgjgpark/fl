//* Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
//*
//* Licensed under the Apache License, Version 2.0 (the "License").
//* You may not use this file except in compliance with the License.
//* A copy of the License is located at
//*
//*  http://aws.amazon.com/apache2.0
//*
//* or in the "license" file accompanying this file. This file is distributed
//* on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
//* express or implied. See the License for the specific language governing
//* permissions and limitations under the License.

var
    AWS = require("aws-sdk"),
    DDB = new AWS.DynamoDB({
        apiVersion: "2012-08-10",
        region: "ap-northeast-2"
    });

(function uploadItemstoDynamoDB(){
    var
        org_1 = {
            Item:{
                "PK":{
                    S: "ORG#1"
                },
                "SK":{
                    S: "ORG#1"
                },	
                "type":{
                    S: "Organization"
                },
                "orgId":{
                    S: "1"
                },
                "name":{
                    S: "세브란스병원" 
                },
                "description":{
                    S: "연세 세브란스 병원" 
                }
            },
            ReturnConsumedCapacity: "TOTAL",
            TableName: "federated-learning-table"
        };
     DDB.putItem(org_1, function(err, data){
         console.log(err, data);
     });
     var
        org_2 = {
            Item:{
                "PK":{
                    S: "ORG#2"
                },
                "SK":{
                    S: "ORG#2"
                },	
                "type":{
                    S: "Organization"
                },
                "orgId":{
                    S: "2"
                },
                "name":{
                    S: "삼성서울병원" 
                },
                "description":{
                    S: "삼성 서울 병원" 
                }
            },
            ReturnConsumedCapacity: "TOTAL",
            TableName: "federated-learning-table"
        };
     DDB.putItem(org_2, function(err, data){
         console.log(err, data);
     });
})();
