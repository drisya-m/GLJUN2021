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
from utils import *


def handler(event, context):
    body = get_request_body_json(event)
    print(body)
    # db connection
    db_driver: DatabaseDriver = get_db_driver()
    db_driver.create_user_record(user=body)
    return respond(200, "hello world", {})

body = {"username":"drisya"}
event = {
  "isBase64Encoded": False,
  "headers": {
  }
}
event["body"] = json.dumps(json.dumps(body))
print(handler(event, None))