import boto3

from .creds import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def get_s3_client() -> None:
    """Connect to s3 & return client"""

    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return session.client('s3')
