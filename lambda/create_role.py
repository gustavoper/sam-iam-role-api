import json
import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    role_name = body.get('role_name')
    if not role_name:
        return {"statusCode": 400, "body": json.dumps({"error": "role_name inexistente"})}
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }


    try:
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description="Role criada por Lambda"
        )

        iam.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess'
        )

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Role criada com sucesso",
                "arn": response['Role']['Arn']
            })
        }

    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            return {"statusCode": 409, "body": json.dumps({"message": "Role ja existe!"})}
        raise