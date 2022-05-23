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
import json
from typing import Optional

import paho.mqtt.client
import requests
from jwthelper import JwtHelper
from mqtthelper import MqttClient


class ApiClient:
    # URI for server
    uri: str
    # Secret given by server
    secret: str
    # taxi id given by server
    taxi_id: str
    # name of the user
    name: str
    # license
    license: str
    # type
    taxi_type: str
    # topic
    topic: str
    # mqtt host
    mqtt_host: str
    # mqtt client
    mqtt_client: MqttClient

    def __init__(self, uri: str, name: str, license: str, taxi_type: str):
        self.uri = uri
        self.name = name
        self.license = license
        self.taxi_type = taxi_type

    def register(self):
        print(f'registering a new taxi for {self.name}')
        request_url = f'{self.uri}/register'
        payload = {
            "type": "taxi",
            "name": self.name,
            "taxi_type": self.taxi_type,
            "license": self.license
        }
        response = requests.request(method="POST", url=request_url, json=payload,
                                    headers={'Content-Type': 'application/json'})
        data: dict = response.json()
        self.taxi_id = data['taxi_id']
        self.secret = data['secret']
        print(f'{self.name} registered with taxi id {self.taxi_id} and secret {self.secret}')

    def send_authenticated(self, path: str, body: Optional[dict]):
        request_url = f'{self.uri}/{path}'
        helper = JwtHelper(secret=self.secret)
        token = helper.create_jwt(identity=self.taxi_id, minutes=2)
        response = requests.request(method="POST", url=request_url, json=body,
                                    headers={'Content-Type': 'application/json',
                                             'X-Taxi-Id': self.taxi_id,
                                             'X-Token': token})
        return response.json()

    def login(self):
        print(f'{self.taxi_id}/{self.name} trying to login')
        data: dict = self.send_authenticated('login', None)
        print(f'server responded to login request with {data}')
        self.mqtt_host = data['host']
        self.topic = data['topic']

        # Create a responder
        def message_responder(client, userdata, message):
            self.ride_request_handler(message)

        self.mqtt_client = MqttClient(host=self.mqtt_host)
        self.mqtt_client.connect()
        self.mqtt_client.subscribe(topic=self.topic, fn=message_responder)

    def logoff(self):
        print(f'{self.taxi_id}/{self.name} trying to logoff')
        data: dict = self.send_authenticated('logoff', None)
        print(f'server responded to logoff request with {data}')
        self.mqtt_host = ''
        self.topic = ''
        self.mqtt_client.close()

    def location(self, latitude, longitude):
        print(f'{self.taxi_id}/{self.name} trying to send location')
        data: dict = self.send_authenticated('location', {'location': [latitude, longitude]})
        print(f'server responded to location request with {data}')

    def ride_request_handler(self, message: paho.mqtt.client.MQTTMessage):
        print(f'taxi {self.taxi_id} has read a message from mqtt')
        body: dict = json.loads(message.payload)
        print(body)
