import aws_cdk as cdk
from aws_cdk import aws_appsync, aws_ec2, aws_lambda

app = cdk.App()
stack = cdk.Stack(app, "test-private-appsync-stack")

# VPC
vpc = aws_ec2.Vpc(
    stack,
    "Vpc",
    cidr="10.123.0.0/16",
    max_azs=1,
    subnet_configuration=[
        aws_ec2.SubnetConfiguration(
            name="PublicSubnet",
            subnet_type=aws_ec2.SubnetType.PUBLIC,
        ),
        aws_ec2.SubnetConfiguration(
            name="PrivateSubnet",
            subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT,
        ),
    ],
)
# appsync

## データソース
function = aws_lambda.Function(
    stack,
    "Function",
    runtime=aws_lambda.Runtime.PYTHON_3_9,
    architecture=aws_lambda.Architecture.ARM_64,
    code=aws_lambda.Code.from_asset("runtime"),
    handler="index.handler",
)

## API
api = aws_appsync.GraphqlApi(
    stack,
    "Api",
    name="test-private-appsync",
    schema=aws_appsync.SchemaFile.from_asset("./schema.graphql"),
)
lambda_data_source = aws_appsync.LambdaDataSource(
    stack,
    "LambdaDataSource",
    api=api,
    lambda_function=function,
)
lambda_data_source.create_resolver("QueryGetUsers", type_name="Query", field_name="getUsers")

## 無理やりprivateに設定する
cfn_api: aws_appsync.CfnGraphQLApi = api.node.default_child
cfn_api.visibility = "PRIVATE"

app.synth()
