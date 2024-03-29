"""
Credentials are stored in Lambda env vars
"""
import os

BOT_API_TOKEN = os.environ.get('BOT_API_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

BUCKET_DAGS = os.environ.get('BUCKET_DAGS')     # should include different paths for base and active copies
