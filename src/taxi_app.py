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
import argparse
import random

from joblib import Parallel, delayed

from core import LocationBound
from clients.taxi import TaxiApiClient

# taxi types
TAXI_TYPES = ['MINI', 'ECONOMY', 'SEDAN', 'LUXURY', 'ROYAL']

# Initializing Parser
parser = argparse.ArgumentParser(description='taxi client')
parser.add_argument('--count', type=int, help='number of taxi to run')
parser.add_argument('--uri', type=str, help='server url to connect to')
parser.add_argument('--latitude-min', type=str, help='minimum latitude to run with')
parser.add_argument('--latitude-max', type=str, help='maximum latitude to run with')
parser.add_argument('--longitude-min', type=str, help='minimum longitude to run with')
parser.add_argument('--longitude-max', type=str, help='maximum longitude to run with')
args = parser.parse_args()


def get_taxi_type() -> str:
    return random.choice(TAXI_TYPES)


def get_license() -> str:
    var1 = random.randint(1200, 9999)
    var2 = random.randint(10, 99)
    return f"KA/{var1}/{var2}"


# create bound
bound = LocationBound()
bound.min_latitude = float(args.latitude_min)
bound.max_latitude = float(args.latitude_max)
bound.min_longitude = float(args.longitude_min)
bound.max_longitude = float(args.longitude_max)

taxi_clients = list()
for index in range(0, args.count):
    name = f'taxi-{index}'
    client = TaxiApiClient(uri=args.uri, name=name, license=get_license(), taxi_type=get_taxi_type(), bound=bound)
    client.register()
    taxi_clients.append(client)
Parallel(n_jobs=args.count, backend='threading')(delayed(client.start)() for client in taxi_clients)
