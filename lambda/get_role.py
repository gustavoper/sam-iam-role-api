import json
import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')

def lambda_handler(event, context):
    role_name = event['pathParameters']['name']

    try:
        role = iam.get_role(RoleName=role_name)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "role_name": role['Role']['RoleName'],
                "arn": role['Role']['Arn'],
                "created": role['Role']['CreateDate'].isoformat()
            })
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return {"statusCode": 404, "body": json.dumps({"error": "Role not found"})}
        raise