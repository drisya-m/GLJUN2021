#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Nilotpal Sarkar
# @since 2022.06
#

from clients.taxi import TaxiApiClient
from utils import *
from core import DatabaseDriver


def update_location_for_all_taxi():
    db_driver: DatabaseDriver = get_db_driver()
    taxi_list: [] = db_driver.list_all_taxis()

    for taxi in taxi_list:
        taxiApiClient = TaxiApiClient(uri=args.uri, taxi_id=taxi['taxi_id'], secret=taxi["secret"])
        taxiApiClient.start()



