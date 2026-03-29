import json
import os
import re
import requests

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_file_contents(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def get_file_size(file_path):
    return os.path.getsize(file_path)

def get_env_var(var_name):
    return os.environ.get(var_name)

def get_aws_region():
    return os.environ.get('AWS_REGION')

def get_aws_account_id():
    return os.environ.get('AWS_ACCOUNT_ID')

def get_aws_access_key_id():
    return os.environ.get('AWS_ACCESS_KEY_ID')

def get_aws_secret_access_key():
    return os.environ.get('AWS_SECRET_ACCESS_KEY')

def send_slack_message(channel, message):
    url = f'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': f'Bearer {os.environ.get("SLACK_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    data = {
        'channel': channel,
        'text': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception(f'Slack message failed with status code {response.status_code}')

def validate_required_env_vars(required_vars):
    for var in required_vars:
        if not get_env_var(var):
            raise Exception(f'Missing required environment variable {var}')

def validate_aws_credentials():
    required_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION']
    validate_required_env_vars(required_vars)

def validate_aws_region():
    region = get_aws_region()
    if not re.match(r'^[a-zA-Z]{2}-\d{1}$', region):
        raise Exception('Invalid AWS region')