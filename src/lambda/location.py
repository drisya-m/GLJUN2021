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
    # Get Taxi Id
    taxi_id = get_taxi_id(event)
    # create database helper
    db_driver: DatabaseDriver = get_db_driver()
    existing_taxi = db_driver.get_taxi(taxi_id=taxi_id)
    # if no taxi found, return 401
    if not existing_taxi:
        return unauthorized()
    # validate jwt
    if not validate_token(event, identity=taxi_id, secret=existing_taxi['secret']):
        return unauthorized()
    # extract body for location
    body: dict = get_request_body_json(event)
    # find co-ordinates
    location: list = body.get('location')
    if not isinstance(location, list) or len(location) != 2:
        return bad_request()
    # make sure we have correct longitude and latitude
    if not is_valid_location(location[0], location[1]):
        return bad_request()
    # patch location co-ordinates for taxi
    patch_succeeded = db_driver.patch_taxi(taxi_id=taxi_id, patch={
        "location": {
            "type": "Point",
            "coordinates": location
        }})
    if not patch_succeeded:
        return server_error()
    print(f"location update request from taxi {taxi_id} with location {location}")
    return ok_request()
