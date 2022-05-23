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
import json
import random

import paho.mqtt.client
from paho.mqtt import client as mqtt_client
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties


class MqttClient:

    # host
    host: str
    # port
    port: int
    # client-id
    client_id: object
    # client
    client: paho.mqtt.client.Client

    def __init__(self, host: str, port: int = 1883):
        self.host = host
        self.port = port
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

    def connect(self):
        client = mqtt_client.Client(self.client_id)
        client.connect(self.host, self.port)
        self.client = client

    def send_to_topic(self, topic: str, message: dict):
        properties = Properties(PacketTypes.PUBLISH)
        properties.MessageExpiryInterval = 150
        print(f'sending message to topic {topic} {json.dumps(message)}')
        self.client.publish(topic=topic, payload=json.dumps(message), retain=True, properties=properties)
