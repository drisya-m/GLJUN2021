#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Nilotpal Sarkar
# @since 2022.05
#
import random
import time
from random import uniform

from apiclient import ApiClient

USER_COUNT = 1
MAX_LATITUDE = 60
MAX_LONGITUDE = 60
SERVER_URI = 'http://127.0.0.1:5000'
TAXI_TYPES = ['MINI', 'ECONOMY', 'SEDAN', 'LUXURY', 'ROYAL']


def get_taxi_type() -> str:
    return random.choice(TAXI_TYPES)


def get_license() -> str:
    var1 = random.randint(1200, 9999)
    var2 = random.randint(10, 99)
    return f"KA/{var1}/{var2}"


for index in range(0, USER_COUNT):
    name = f'taxi driver {index}'
    client = ApiClient(uri=SERVER_URI, name=name, license=get_license(), taxi_type=get_taxi_type())
    client.register()
    client.login()
    client.location(uniform(-180, 180), uniform(-90, 90))
    # client.logoff()
    client.mqtt_client.client.loop_forever()

