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
const {v4}  = require('uuid')
var
    AWS = require("aws-sdk"),
    DDB = new AWS.DynamoDB({
        apiVersion: "2012-08-10",
        region: "ap-northeast-2"
    });

(function uploadItemstoDynamoDB(){
    var cdm1uuid = v4()
    var cdm2uuid = v4()
    var
        cdm_1 = {
            Item:{
                "PK":{
                    S: "ORG#1"
                },
                "SK":{
                    S: "CDM#"+ cdm1uuid
                },	
                "type":{
                    S: "CDM"
                },
                "cdmId":{
                    S: cdm1uuid
                },
                "name":{
                    S: "세브란스병원CDM" 
                },
                "Description":{
                    S: "연세 세브란스 병원CDM" 
                },
		"GSI1PK": "ALL_CDM",
		"GSI1SK": "CDM#"+ cdm1uuid		
		
            },
            ReturnConsumedCapacity: "TOTAL",
            TableName: "federated-learning-table"
        };
     DDB.putItem(cdm_1, function(err, data){
         console.log(err, data);
     });
     var
        cdm_2 = {
            Item:{
                "PK":{
                    S: "ORG#2"
                },
                "SK":{
                    S: "CDM#"+cdm2uuid
                },	
                "type":{
                    S: "CDM"
                },
                "cdmId":{
                    S: cdm2uuid
                },
                "name":{
                    S: "삼성서울병원CDM" 
                },
                "description":{
                    S: "삼성 서울 병원CDM" 
                },
		"GSI1PK": "ALL_CDM",
		"GSI1SK": "CDM#"+ cdm2uuid
            },
            ReturnConsumedCapacity: "TOTAL",
            TableName: "federated-learning-table"
        };
     DDB.putItem(cdm_2, function(err, data){
         console.log(err, data);
     });
})();
