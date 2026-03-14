import json
import http.client
import logging
import os
from enum import Enum

from openai import AzureOpenAI
from botocore.exceptions import ClientError
import boto3


class Model(Enum):
    CLAUDE3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"


class Claude3Agent:
    def __init__(self, aws_secret_access_key: str, model: str,
                 aws_access_key_id: str = None, region_name: str = "us-east-1"):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=aws_secret_access_key,
        )
        if model == "SONNET":
            self.model = Model.CLAUDE3_SONNET
        elif model == "HAIKU":
            self.model = Model.CLAUDE3_HAIKU
        else:
            raise ValueError("Invalid model type. Please choose from 'SONNET' or 'HAIKU' models.")

    def invoke(self, text: str, **kwargs) -> str:
        try:
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "messages": [
                        {"role": "user", "content": [{"type": "text", "text": text}]}
                    ],
                    **kwargs
                }
            )
            response = self.client.invoke_model(modelId=self.model.value, body=body)
            completion = json.loads(response["body"].read())["content"][0]["text"]
            return completion
        except ClientError:
            logging.error("Couldn't invoke model")
            raise


class ContentFormatter:
    @staticmethod
    def chat_completions(text, settings_params):
        message = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ]
        data = {"messages": message, **settings_params}
        return json.dumps(data)


class AzureAgent:
    def __init__(self, api_key, azure_uri, deployment_name):
        self.azure_uri = azure_uri
        self.headers = {
            'Authorization': f"Bearer {api_key}",
            'Content-Type': 'application/json'
        }
        self.deployment_name = deployment_name
        self.chat_formatter = ContentFormatter

    def invoke(self, text, **kwargs):
        body = self.chat_formatter.chat_completions(text, {**kwargs})
        conn = http.client.HTTPSConnection(self.azure_uri)
        conn.request("POST", '/v1/chat/completions', body=body, headers=self.headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        decoded_data = data.decode("utf-8")
        parsed_data = json.loads(decoded_data)
        content = parsed_data["choices"][0]["message"]["content"]
        return content


class GPTAgent:
    def __init__(self, api_key, azure_endpoint, deployment_name, api_version):
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        self.deployment_name = deployment_name

    def invoke(self, text, **kwargs):
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ],
            **kwargs
        )
        return response.choices[0].message.content
