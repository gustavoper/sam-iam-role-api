import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from create_role import lambda_handler
from botocore.exceptions import ClientError
from datetime import datetime,timezone

import json
from unittest.mock import patch
from get_role import lambda_handler

@patch("get_role.iam")
def test_get_role_success(mock_iam):
    mock_iam.get_role.return_value = {
        "Role": {
            "RoleName": "MinhaNovaRole",
	        "Arn": "arn:aws:iam::123456796:role/MinhaNovaRole",
            "CreateDate": datetime(2025, 7, 31, 3, 13, 57, tzinfo=timezone.utc)
            }
        
    }

    event = {"pathParameters": {"name": "MinhaNovaRole"}}
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["role_name"] == "MinhaNovaRole"

@patch("get_role.iam")
def test_get_role_not_found(mock_iam):
    mock_iam.get_role.side_effect = ClientError(
        error_response={"Error": {"Code": "NoSuchEntity"}},
        operation_name="GetRole"
    )

    event = {"pathParameters": {"name": "UnknownRole"}}
    response = lambda_handler(event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 404
    assert body["error"] == "Role not found"
