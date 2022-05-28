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
from random import uniform
from joblib import Parallel, delayed

from clients.user import UserApiClient
from core import LocationBound


def bound():
    bound = LocationBound()
    bound.min_latitude = 12.87
    bound.max_latitude = 13.21
    bound.min_longitude = 77.34
    bound.max_longitude = 77.87
    return bound


USER_COUNT = 1
MAX_LATITUDE = 60
MAX_LONGITUDE = 60
SERVER_URI = 'http://127.0.0.1:5000'

user_list = list()

for index in range(0, USER_COUNT):
    name = f'user-{index}'
    client = UserApiClient(uri=SERVER_URI, name=name, bound=bound())
    client.register()
    user_list.append(client)

Parallel(n_jobs=USER_COUNT, backend='threading')(delayed(client.ride)() for client in user_list)
