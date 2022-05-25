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

from joblib import Parallel, delayed

from core import LocationBound
from clients.taxi import TaxiApiClient

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


def bound():
    bound = LocationBound()
    bound.min_latitude = 12.87
    bound.max_latitude = 13.21
    bound.min_longitude = 77.34
    bound.max_longitude = 77.87
    return bound


taxi_clients = list()
for index in range(0, USER_COUNT):
    name = f'taxi-{index}'
    client = TaxiApiClient(uri=SERVER_URI, name=name, license=get_license(), taxi_type=get_taxi_type(), bound=bound())
    client.register()
    taxi_clients.append(client)
Parallel(n_jobs=USER_COUNT, backend='threading')(delayed(client.start)() for client in taxi_clients)
