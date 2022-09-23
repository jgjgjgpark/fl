aws dynamodb query \
--table-name federated-learning-table \
--index-name globalIndex2 \
--key-condition-expression "GSI1PK = :value" \
--expression-attribute-values '{":value":{"S":"ALL_CDM"}}' \
--projection-expression "cdmId, description"