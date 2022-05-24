#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Drisya Mathilakath
# @since 2022.05
#
import random

from apiclient import ApiClient
import uuid
import random


TAXI_COUNT = 50
SERVER_URI = 'http://127.0.0.1:5000'

for index in range(0, TAXI_COUNT):
    name = f'taxi driver {index}'
    license = uuid.uuid4().hex[:6].upper()
    category = random.choice(ApiClient.taxi_types())
    client = ApiClient(uri=SERVER_URI, name=name, license=license, category= category)
    client.register()
