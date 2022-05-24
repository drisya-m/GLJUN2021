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
from jwthelper import JwtHelper

class ApiClient:
    #URI for server
    uri : str
    #secret given by server
    secret: str
    #taxi number
    taxi_id: str


    def __init__(self, uri: str, license: str, name: str, category: str):
        self.uri = uri
        self.license = license
        self.name = name
        self.category = category


    def register(self):
        print(f'registering new taxi for {self.taxi_id}')
        request_url = f'{self.uri}/register'
        payload = {'type': 'taxi', 'license': self.license, 'name': self.name, 'category': self.category}
        response = requests.request(method="POST", url=request_url, json=payload,
                                    headers={'Content-Type': 'application/json'})

        data: dict = response.json()
        self.taxi_id = data['taxi_id']
        self.secret = data['secret']
        print(f'{self.license} registered with user id {self.taxi_id} and secret {self.secret}')

    def taxi_types(self) -> set:
        return {'MINI', 'ECONOMY', 'SEDAN', 'LUXURY', 'ROYAL'}

