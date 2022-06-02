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

import requests
from core.jwthelper import JwtHelper
import json
from core import *


class ApiClient:
    # URI for server
    uri: str
    # Secret given by server
    secret: str
    # user id given by server
    user_id: str
    # name of the user
    name: str
    #ride_id of the ride request
    ride_id: str
    # ride_topic
    ride_topic: str

    def __init__(self, uri: str, name: str):
        self.uri = uri
        self.name = name

    def register(self):
        print(f'registering a new user for {self.name}')
        request_url = f'{self.uri}/register'
        payload = {"type": "user", "name": self.name}
        response = requests.request(method="POST", url=request_url, json=payload,
                                    headers={'Content-Type': 'application/json'})
        data: dict = response.json()
        self.user_id = data['user_id']
        self.secret = data['secret']
        #print(data)
        print(f'{self.name} registered with user id {self.user_id} and secret {self.secret}')

    def createride(self, longitude, latitude):
        self.latitude = latitude
        self.longitude = longitude
        print(f'{self.user_id}/{self.name} creating ride request from location {latitude} and {longitude}')
        request_url = f'{self.uri}/createride'
        helper = JwtHelper(secret=self.secret)
        token = helper.create_jwt(identity=self.user_id, minutes=2)
        payload = {'user_id': self.user_id, 'location': [longitude, latitude]}
        response = requests.request(method="POST", url=request_url, json=payload,
                                    headers={'Content-Type': 'application/json',
                                             'X-User-Id': self.user_id,
                                             'X-Token': token})
        data: dict = response.json()
        self.ride_id = data['ride_id']
        self.ride_topic = data['topic']
        print(f'Response from createride {data}')


    def find_taxi(self):
        print(f'{self.user_id}/{self.name} trying to find a taxi from location {self.latitude} and {self.longitude}')
        request_url = f'{self.uri}/findtaxi'
        helper = JwtHelper(secret=self.secret)
        token = helper.create_jwt(identity=self.user_id, minutes=2)
        payload = {'user_id': self.user_id, 'ride_id': self.ride_id}
        response = requests.request(method="POST", url=request_url, json=payload,
                                    headers={'Content-Type': 'application/json',
                                             'X-User-Id': self.user_id,
                                             'X-Token': token})
        data: dict = response.json()
        print(f'Server responded with {data}')
