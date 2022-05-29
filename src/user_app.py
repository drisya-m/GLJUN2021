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
import argparse
import random
from random import uniform
from joblib import Parallel, delayed

from clients.user import UserApiClient
from core import LocationBound

# Initializing Parser
parser = argparse.ArgumentParser(description='taxi client')
parser.add_argument('--count', type=int, help='number of taxi to run')
parser.add_argument('--uri', type=str, help='server url to connect to')
parser.add_argument('--latitude-min', type=str, help='minimum latitude to run with')
parser.add_argument('--latitude-max', type=str, help='maximum latitude to run with')
parser.add_argument('--longitude-min', type=str, help='minimum longitude to run with')
parser.add_argument('--longitude-max', type=str, help='maximum longitude to run with')
args = parser.parse_args()

# create bound
bound = LocationBound()
bound.min_latitude = float(args.latitude_min)
bound.max_latitude = float(args.latitude_max)
bound.min_longitude = float(args.longitude_min)
bound.max_longitude = float(args.longitude_max)


user_list = list()
for index in range(0, args.count):
    name = f'user-{index}'
    client = UserApiClient(uri=args.uri, name=name, bound=bound)
    client.register()
    user_list.append(client)

Parallel(n_jobs=args.count, backend='threading')(delayed(client.ride)() for client in user_list)
