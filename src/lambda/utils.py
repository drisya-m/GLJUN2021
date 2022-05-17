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

import json


def respond(code: Optional[int], body=None, headers=None):
    """ Utility method to generate json response for a lambda call"""
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
