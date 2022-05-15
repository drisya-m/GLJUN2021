#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Anirudh Kushwah
# @since 2022.05
#
from typing import Optional

import boto3
import json

dynamo = boto3.client('dynamodb')


def respond(code: Optional[int], body=None, headers=None):
    heads = {
        'Content-Type': 'application/json',
    }
    if heads is not None:
        heads.update(headers)
    return {
        'statusCode': str(code),
        'body': json.dumps(body),
        'headers': heads,
    }


def handler(event, context):
    print(event)
    return respond(200, "hello world", {})
