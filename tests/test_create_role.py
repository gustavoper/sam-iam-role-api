import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from create_role import lambda_handler
import json
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError

from create_role import lambda_handler

@patch("create_role.iam")
def test_create_role_success(mock_iam):
    mock_iam.create_role.return_value = {
        "Role": {"Arn": "arn:aws:iam::123456789012:role/TestRole"}
    }

    event = {
        "body": json.dumps({"role_name": "TestRole"})
    }

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 201


@patch("create_role.iam")
def test_create_role_already_exists(mock_iam):
    mock_iam.create_role.side_effect = ClientError(
        error_response={
            "Error": {"Code": "EntityAlreadyExists", "Message": "Role já existe!"}
        },
        operation_name="CreateRole"
    )

    event = {"body": json.dumps({"role_name": "ExistingRole"})}

    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 409
    assert body["message"] == "Role ja existe!"