import enum
import json
import logging
from os import path

import boto3
from botocore.exceptions import ClientError


class ConfigClient:
    def __init__(self):
        self.configuration = self.retrieve_config()
        self.credentials = self.retrieve_credentials()

    @staticmethod
    def retrieve_config():
        filepath = "config.json"

        if not path.exists(filepath):
            raise FileNotFoundError

        with open(filepath) as json_data_file:
            return json.load(json_data_file)

    @staticmethod
    def retrieve_credentials():
        return CredentialClient.mock_credentials()

    def get_config_by_name(self, name):
        if name not in self.configuration['client_config'].keys():
            logging.error("No defined key in config for name: ", name)

        else:
            return self.configuration['client_config'][name]


class CredentialClient:
    def __init__(self, region, key_id, key):
        self.region = region
        self.key_id
        self.key

    @staticmethod
    def mock_credentials():
        return {"jira": "jira_key", "s3": "s3_key"}

    def retrieve_config(self):
        secret_name = "MySecretName"

        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=self.region,
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("The requested secret " + secret_name + " was not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("The request was invalid due to:", e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("The request had invalid params:", e)
        else:
            # Secrets Manager decrypts the secret value using the associated KMS CMK
            # Depending on whether the secret was a string or binary, only one of these fields will be populated
            if 'SecretString' in get_secret_value_response:
                text_secret_data = get_secret_value_response['SecretString']
            else:
                binary_secret_data = get_secret_value_response['SecretBinary']


class ClientName(enum.Enum):
    jira = 'jira'
    s3 = 's3'
    # Add more script names here
