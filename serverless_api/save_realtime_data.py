import json
import os

from jsonschema import validate
import jsonschema
import boto3

s3 = boto3.client('s3')


def lambda_handler(event, context):
    real_time_stock_data_schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "type": "object",
        "properties": {
            "Service": {
                "type": "object",
                "properties": {
                    "timestamp": {
                        "type": "string"
                    },
                    "Symbol": {
                        "type": "string"
                    },
                    "Company": {
                        "type": "string"
                    },
                    "Price": {
                        "type": "number"
                    },
                    "Change": {
                        "type": "number"
                    },
                    "Change%": {
                        "type": "string"
                    },
                    "Volume": {
                        "type": "integer"
                    }
                },
                "required": [
                    "timestamp",
                    "Symbol",
                    "Company",
                    "Price",
                    "Change",
                    "Change%",
                    "Volume"
                ]
            }
        },
        "required": [
            "Service"
        ]
    }

    try:
        event = json.loads(event['body'])
        validate(instance=event, schema=real_time_stock_data_schema)
    except jsonschema.ValidationError as e:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'message': f'JSON Validation error: {e.json_path}: {e.message}'})
        }

    s3_bucket_name = 'ck-portfolio-bucket'
    object_key = 'processed/data.json'
    s3.put_object(
        Bucket=s3_bucket_name,
        Key=object_key,
        Body=json.dumps(event)
    )

    response = {
        'success': 'File is successfully uploaded to s',
    }

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response)
    }
