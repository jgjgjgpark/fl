import {Stack, StackProps} from "aws-cdk-lib";
import {Construct} from "constructs";
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
import {readFileSync} from "fs";
import {ManagedPolicy, Policy, PolicyDocument, PolicyStatement, Role, ServicePrincipal} from "aws-cdk-lib/aws-iam";

export class FederatedLearningStack extends Stack {
    constructor(scope: Construct, id: string, props?: StackProps) {
        super(scope, id, props);
        const vpc = this.createVpc();
        const webSG = this.createSecurityGroup(vpc);

        const s3Policy = new PolicyDocument({
            statements: [
                new PolicyStatement({
                    resources: ['*'],
                    actions: ['s3:*'],
                }),
            ],
        });

        const role = new Role(this, 'webserver-role', {
            assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
            inlinePolicies: {
                s3Policy
            },
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'),
            ],
        });

        role.attachInlinePolicy(
            new Policy(this, 'cw-logs', {
                statements: [
                    new PolicyStatement({
                        actions: ['s3:*'],
                        resources: ['*'],
                    }),
                ],
            }),
        );
        this.createEc2(vpc, webSG, role);
    }

    private createEc2(vpc: Vpc, webSG: SecurityGroup, role: Role) {
        const ec2Instance = new Instance(this, 'instance', {
            vpc,
            vpcSubnets: {
                subnetType: SubnetType.PUBLIC
            },
            role,
            securityGroup: webSG,
            instanceType: InstanceType.of(InstanceClass.BURSTABLE2, InstanceSize.MICRO),
            machineImage: new AmazonLinuxImage({
                generation: AmazonLinuxGeneration.AMAZON_LINUX_2
            }),
            keyName: 'federated'
        })
        // load user data script
        const userDataScript = readFileSync('./infrastructure/user-data.sh', 'utf-8')
        ec2Instance.addUserData(userDataScript)
        ec2Instance.addToRolePolicy(new PolicyStatement({
            actions: ['s3:*'],
            resources: ['*'],
        }))
    }

    private createSecurityGroup(vpc: Vpc) {
        const webSG = new SecurityGroup(this, 'web_sq', {
            vpc,
            allowAllOutbound: true,
        })
        webSG.addIngressRule(Peer.anyIpv4(), Port.tcp(80), 'allow http traffic')
        webSG.addIngressRule(Peer.anyIpv4(), Port.tcp(22), 'allow ssh traffic')
        return webSG;
    }

    private createVpc() {
        const vpc = new Vpc(this, 'org1-vpc', {
            cidr: '10.1.0.0/16',
            natGateways: 0
        })
        return vpc;
    }
}