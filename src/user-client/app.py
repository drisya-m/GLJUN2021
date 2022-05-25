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
from random import uniform
import argparse
from apiclient import ApiClient

USER_COUNT = 20
MAX_LATITUDE = 60
MAX_LONGITUDE = 60
SERVER_URI = 'http://127.0.0.1:5000'

# Initializing Parser
parser = argparse.ArgumentParser(description='User Registration')

#Adding argument
parser.add_argument('--count', type=int, help='user count')
parser.add_argument('--uri', type=str, help='server uri')
parser.add_argument('--latitude', type=int, nargs='+', help='min and max latitude')
parser.add_argument('--longitude', type=int, nargs='+', help='min and max longitude')
args = parser.parse_args()
print(args)

user_list = list()

for index in range(0, USER_COUNT):
    name = f'taxi user {index}'
    client = ApiClient(uri=SERVER_URI, name=name)
    client.register()
    #latitude, longitude = uniform(-180, 180), uniform(-90, 90)
    latitude, longitude = uniform(-180, MAX_LATITUDE), uniform(-90, MAX_LONGITUDE)
    client.find_taxi(latitude, longitude)
    user_list.append(client)
