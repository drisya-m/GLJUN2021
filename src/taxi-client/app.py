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
import argparse


# Initializing Parser
parser = argparse.ArgumentParser(description='Taxi Registration')

#Adding argument
parser.add_argument('--count', type=int, help='taxi count')
parser.add_argument('--uri', type=str, help='server uri')
args = parser.parse_args()

taxi_count = args.count
server_uri = args.uri

for index in range(0, taxi_count):
    name = f'taxi driver {index}'
    license = uuid.uuid4().hex[:6].upper()
    category = random.choice(ApiClient.taxi_types())
    client = ApiClient(uri=server_uri, name=name, license=license, category= category)
    client.register()
