# -*- coding: utf-8 -*-
import boto3
import base64
import logging
import os

import trawsate

kms = boto3.client('kms')

logger = logging.getLogger(__name__)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)


def _kms_decrypt(ciphertext: str) -> bytes:
    """
    Decrypt a value using KMS.

    :param ciphertext: The base64-encoded ciphertext.
    :return: The plaintext bytestring.
    """
    return kms.decrypt(
        CiphertextBlob=base64.b64decode(ciphertext))['Plaintext']


def _kms_decrypt_str(ciphertext: str, encoding: str = 'utf-8') -> str:
    """
    Decrypt a piece of text using KMS.

    :param ciphertext: The base64-encoded ciphertext.
    :param encoding: The encoding of the text.
    :return: The plaintext.
    """
    return _kms_decrypt(ciphertext).decode(encoding)


_TRAVIS_ACCESS_TOKEN = _kms_decrypt_str(os.environ['TRAVIS_ACCESS_TOKEN'])


# noinspection PyUnusedLocal
def handler(event, context) -> None:
    """
    AWS Lambda entry point.

    :param event: The event that triggered this execution.
    :param context: Current runtime information: http://docs.aws.amazon.com
                    /lambda/latest/dg/python-context-object.html.
    """
    logger.info(f'Event: {event}')
    rotator = trawsate.Rotator(_TRAVIS_ACCESS_TOKEN)
    for result in rotator.keys(event['config'], 30):
        logger.info(result)
