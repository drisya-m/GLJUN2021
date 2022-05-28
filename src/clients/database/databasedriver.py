#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Shanger Sivaramachandran
# @since 2022.05
import mongodbconnection
import time


class DatabaseDriver():
    # database_name
    database_name = "taxi_service"

    # Create database if doesn't exist.
    def create_database_with_collections(self):
        cli = self.get_db_connection()
        with cli:
            db = cli.connection[self.database_name]
            db['taxi_profile']
            db['user_profile']
            db['taxi_location_history']
            db['taxi_request_history']

    def get_db_connection(self):
        cli = mongodbconnection.MongoDBConnection()
        return cli

    # get taxi record by id
    def get_taxi(self, taxi_id: str) -> dict:
        cli = self.get_db_connection()
        with cli:
            db = cli.connection[self.database_name]
            return dict(db['taxi_profile'].find({taxi_id: taxi_id}))

    # insert new taxi record here, return Id
    def create_taxi_record(self, taxi: dict) -> str:
        cli = self.get_db_connection()
        with cli:
            db = cli.connection['taxi_service']
            db['taxi_profile'].insert_one(taxi)

    def update_taxi_record(self, taxi_id: str, patch: dict):
        cli = self.get_db_connection()
        with cli:
            db = cli.connection['taxi_service']
        # @TODO patch the records
        return True

    def find_nearby_taxi(self, location: dict, radius: float, limit: int) -> list:
        metersPerKiloMeter = 1000
        cli = self.get_db_connection()
        with cli:
            db = cli.connection[self.database_name]
            taxi_list = db['taxi_profile'].find({
                "location": location,
                "taxiOnDuty": False,
                "ActiveTaxi": True,
                "maxDistance": radius * metersPerKiloMeter})

            nearByTaxiList = []
            # @TODO return list of all taxi_ids
            for taxi in range(limit - 1):
                for taxi_id in taxi_list:
                    nearByTaxiList.append(nearByTaxiList)
            return nearByTaxiList

    # return list of all taxi records
    def list_all_taxis(self) -> list:
        cli = self.get_db_connection()
        with cli:
            db = cli.connection['taxi_service']
            return list(db['taxi_profile'].find())

    # return user record by id.
    def get_user(self, user_id: str) -> dict:
        cli = self.get_db_connection()
        with cli:
            db = cli.connection['user_profile']
            return dict(db['user_profile'].find({user_id: user_id}))

    # insert new user record here, return Id
    def create_user_record(self, user: dict) -> str:
        cli = self.get_db_connection()
        with cli:
            db = cli.connection['user_profile']
            return db['user_profile'].insert_one(user)
