import {CfnOutput, CfnParameter, Stack, StackProps} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import {join} from "path";
import {IResource, LambdaIntegration, RestApi} from "aws-cdk-lib/aws-apigateway";
import {NodejsFunction} from "aws-cdk-lib/aws-lambda-nodejs";
import {Policy, PolicyStatement} from "aws-cdk-lib/aws-iam";
import {
    AmazonLinuxGeneration,
    AmazonLinuxImage,
    Instance,
    InstanceClass,
    InstanceSize,
    InstanceType,
    Peer,
    Port,
    SecurityGroup,
    SubnetType,
    Vpc
} from "aws-cdk-lib/aws-ec2";
import * as s3n from 'aws-cdk-lib/aws-s3-notifications'
import {readFileSync} from "fs";
import {Bucket, EventType} from "aws-cdk-lib/aws-s3";
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb'
import {GenericTable} from "./generic-table";

// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class FederatedLearningStack extends Stack {
    private table: dynamodb.Table;

    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);
        if (props && props.stackName === 'FederatedLearning') {
            this.createServer();
        } else if (props && props.stackName === 'Organization1Stack') {
            this.createOrganization1Server();
        } else {
            this.createDynamoStack()
        }
    }

    private createServer() {
        //create table
        this.table = this.createFederatedLearningTable();

        const api = new RestApi(this, 'fl-api')

        let nodejsFunction = this.createLambda('organization-lambda', 'organization-service.ts');

        const orgResource = this.addResource(
            api.root,
            new LambdaIntegration(nodejsFunction),
            ['organizations'],
            'GET'
        )

        this.addResource(
            orgResource,
            new LambdaIntegration(nodejsFunction),
            ['{orgId}'],
            'GET'
        )

        const analysesResource = this.createAnalysesResource(api.root)
        const analysisResource = analysesResource.addResource("{analysisId}")
        const predefinedUrlResource = this.createPredefinedUrlResource(analysisResource)
        const roundsResource = analysisResource.addResource("rounds")
        const roundResource = this.createRoundResource(roundsResource)
        const cdmResource = this.createCdmResource(api.root)


        // get s3
        const s3Bucket = Bucket.fromBucketName(this, 'federated-learning-bucket', 'federated-learning-bucket')
        s3Bucket.addEventNotification(
            EventType.OBJECT_CREATED,
            new s3n.LambdaDestination(this.createLambda('s3-event-listener', 's3-event-listener.ts')),
            {suffix: '.zip'}
        )
    }

    private createFederatedLearningTable() {
        const table = new dynamodb.Table(this, 'federated-learning-table', {
            tableName: 'federated-learning-table',
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
            partitionKey: {name: 'PK', type: dynamodb.AttributeType.STRING},
            sortKey: {name: 'SK', type: dynamodb.AttributeType.STRING}
        })

        table.addGlobalSecondaryIndex({
            indexName: 'globalIndex1',
            partitionKey: {name: 'PK', type: dynamodb.AttributeType.STRING},
            sortKey: {name: 'SK', type: dynamodb.AttributeType.STRING},
            projectionType: dynamodb.ProjectionType.ALL
        })

        table.addGlobalSecondaryIndex({
            indexName: 'globalIndex2',
            partitionKey: {name: 'GSI1PK', type: dynamodb.AttributeType.STRING},
            sortKey: {name: 'GSI1SK', type: dynamodb.AttributeType.STRING},
            projectionType: dynamodb.ProjectionType.ALL
        })
        return table
    }

    private createAnalysesResource(parent: IResource) {
        const resource = parent.addResource("analyses")
        const integration = new LambdaIntegration(this.createLambda('analysis-lambda', 'analysis-service.ts'))
        resource.addMethod("POST", integration)
        return resource
    }

    private createCdmResource(parent: IResource) {
        const resource = parent.addResource("cdms")
        const integration = new LambdaIntegration(this.createLambda('cdm-lambda', 'cdm-service.ts'))
        resource.addMethod("GET", integration)
        return resource
    }

    private createPredefinedUrlResource(parent: IResource) {
        const resource = parent.addResource("predefined_url")
        const integration = new LambdaIntegration(this.createLambda('presigned-url-lambda',
            'presigned-url-service.ts', this.createS3AllPolicy('s3-full-access-put')))
        resource.addMethod("GET", integration, {
            requestParameters: {
                'method.request.querystring.round': true
            }
        })
        return resource
    }

    private createRoundResource(parent: IResource) {
        const resource = parent.addResource("{round}")
        const integration = new LambdaIntegration(this.createLambda('execution-lambda',
            'execution-service.ts', this.createS3AllPolicy('s3-full-access-get')))
        resource.addMethod("PUT", integration)
        return resource
    }

    createLambda(id: string, fileName: string, policy?: Policy) {
        const lambda = new NodejsFunction(this, id, {
            entry: (join(__dirname, '..', 'src', 'services', fileName)),
            handler: 'handler'
        })
        if (policy) {
            lambda.role?.attachInlinePolicy(policy)
        }
        // add table access to lambda
        this.table.grantFullAccess(lambda)
        return lambda
    }

    createS3AllPolicy(id: string) {
        const policyStatement = new PolicyStatement({
            actions: ['s3:*'],
            resources: ['arn:aws:s3:::*']
        })
        return new Policy(this, id, {
            statements: [policyStatement]
        })
    }

    private addResource(parent: IResource, lambdaIntegration: LambdaIntegration, resourceNames: string[], method: string) {
        let resource = parent
        resourceNames.forEach((resourceName) => {
            resource = resource.addResource(resourceName)
        })
        resource.addMethod(method, lambdaIntegration)
        return resource
    }

    /**
     * create organization stack
     * @private
     */
    private createOrganization1Server() {
        const vpc = new Vpc(this, 'org1-vpc', {
            cidr: '10.1.0.0/16',
            natGateways: 0
        })
        /*
        const alb = new ApplicationLoadBalancer(this, 'alb', {
            vpc,
            internetFacing: true
        })

        const listener = alb.addListener('Listener', {
            port: 80,
            open: true
        })

        listener.addTargets('default-target', {

        })

         */

        const webSG = new SecurityGroup(this, 'web_sq', {vpc})
        webSG.addIngressRule(Peer.anyIpv4(), Port.tcp(80), 'allow http traffic')
        webSG.addIngressRule(Peer.anyIpv4(), Port.tcp(22), 'allow ssh traffic')

        const ec2Instance = new Instance(this, 'instance', {
            vpc,
            vpcSubnets: {
                subnetType: SubnetType.PUBLIC
            },
            securityGroup: webSG,
            instanceType: InstanceType.of(InstanceClass.BURSTABLE2, InstanceSize.MICRO),
            machineImage: new AmazonLinuxImage({
                generation: AmazonLinuxGeneration.AMAZON_LINUX_2
            }),
            keyName: 'federated',
        })

        // s3 bucket event registration
        const bucket = Bucket.fromBucketName(this, 'federated-learning-bucket', 'federates')
        // bucket.addEventNotification(
        //     EventType.OBJECT_CREATED,
        //     new LambdaDestination()
        // )


        // load user data script
        const userData = readFileSync("./infrastructure/user-data-new.sh", 'utf-8')
        ec2Instance.addUserData(userData)
    }

    private createDynamoStack() {
        // cdk deploy parameters tableName=test
        const tableName = new CfnParameter(this, 'tableName', {
            type: 'String',
            default: 'SessionStoreTable'
        })
        const table = this.createDragonTable();

        new CfnOutput(this, 'arn', {
            value: table.tableArn
        })
    }

    private createDragonTable() {
        const table = new dynamodb.Table(this, 'dragons', {
            tableName: 'dragons',
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
            partitionKey: {name: 'dragon_name', type: dynamodb.AttributeType.STRING}
        })
        return table;
    }
}