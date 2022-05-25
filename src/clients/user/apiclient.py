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
import json
import random

import paho

from core import *


class UserApiClient:
    # URI for server
    server_client: HttpClient
    # Secret given by server
    secret: str
    # name of the user
    name: str
    # user id
    user_id: str
    # topic
    topic: str
    # mqtt client
    mqtt_client: MqttClient
    # logger
    log: Log
    # location box
    bound: LocationBound
    # are you in middle of ride
    ride_in_progress: bool
    # ride count
    ride_remaining: int
    # taxi type
    taxi_type: str

    def __init__(self, uri: str, name: str, bound: LocationBound):
        self.server_client = HttpClient(uri=uri)
        self.name = name
        self.bound = bound
        self.ride_in_progress = False
        self.ride_remaining = 5
        self.taxi_type = random.choice(TAXI_TYPES)
        self.log = Log(name=f'{name}/{self.taxi_type}')

    def send_authenticated(self, path: str, body):
        return self.server_client.send_taxi_request(path, self.user_id, self.secret, body)

    def register(self):
        self.log.log('registering this user with server')
        payload = {
            "type": "user",
            "name": self.name
        }
        data: dict = self.server_client.send_anonymous('register', payload)
        self.user_id = data['user_id']
        self.secret = data['secret']
        self.log.log('registered user: id={} secret={}', self.user_id, self.secret)

    def ride(self):
        current_latitude = random.uniform(self.bound.min_latitude, self.bound.max_latitude)
        current_longitude = random.uniform(self.bound.min_longitude, self.bound.max_longitude)
        self.log.log('ride request: location={}, {} type={}', current_latitude, current_longitude, self.taxi_type)
        payload = {'location': [current_latitude, current_longitude], 'type': self.taxi_type}
        data: dict = self.send_authenticated('find_taxi', payload)

        ride_topic = data.get('topic')
        mqtt_host = data.get('host')
        self.log.log('ride request accepted: topic={} host={}', ride_topic, mqtt_host)

        # wait for message using mqtt client
        mqtt_client = MqttClient(host=mqtt_host, name=self.name)
        mqtt_client.connect()

        # handler for message
        def message_responder(client, userdata, message):
            self.ride_request_handler(mqtt_client, message)

        # wait for responses
        mqtt_client.subscribe(fn=message_responder, topic=ride_topic)
        mqtt_client.client.loop_forever()

    def ride_request_handler(self, mqtt_client: MqttClient, message: paho.mqtt.client.MQTTMessage):
        body: dict = json.loads(message.payload)
        self.log.log('got ride request message: {}', body)
