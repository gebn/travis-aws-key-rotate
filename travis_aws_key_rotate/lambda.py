# -*- coding: utf-8 -*-
import logging
import os

import trawsate

logger = logging.getLogger(__name__)
logging.getLogger('boto3').setLevel(logging.INFO)
logging.getLogger('botocore').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)


_TRAVIS_ACCESS_TOKEN = os.environ['TRAVIS_ACCESS_TOKEN']


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
