import boto3
import json
import os

def get_db_credentials():
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='netflix/db/credentials')
    return json.loads(response['SecretString'])

def get_database_url():
    creds = get_db_credentials()
    host = os.environ.get('DB_HOST')
    return f"mysql+pymysql://{creds['username']}:{creds['password']}@{host}:3306/netflixdb"