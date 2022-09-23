#!/bin/bash

zip -r deploy-app.zip src/ requirements.txt
aws s3 cp deploy-app.zip s3://federated-learning-bucket/org_api_server/deploy-app.zip