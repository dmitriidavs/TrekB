from typing import ClassVar

import boto3

from .log import logger
from .creds import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def get_s3_client() -> ClassVar:
    """Connect to s3 & return client"""

    logger.info('Establishing s3 connection')
    session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    logger.info('Established s3 connection')
    return session.client('s3')


def create_dag_copy(source_bucket: str, source_key: str,
                    destination_bucket: str, destination_key: str) -> None:
    """Create a copy of a base dag"""

    logger.info(f'Creating a new copy of {source_key} - {destination_key} in {destination_bucket}')
    get_s3_client().copy_object(
        CopySource={'Bucket': source_bucket, 'Key': source_key},
        Bucket=destination_bucket,
        Key=destination_key
    )
    logger.info(f'Created a new copy of {source_key} - {destination_key} in {destination_bucket}')
