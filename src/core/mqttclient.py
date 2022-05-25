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

from .log import Log


class MqttClient:
    # host
    host: str
    # port
    port: int
    # client-id
    client_id: object
    # client
    client: paho.mqtt.client.Client
    # logger
    log: Log

    def __init__(self, name: str, host: str, port: int = 1883):
        self.host = host
        self.port = port
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.log = Log(name=f'mqtt-{name}')

    def connect(self):
        self.log.log('connecting to mqtt server')
        client = mqtt_client.Client(self.client_id)
        client.connect(self.host, self.port)
        self.client = client

    def send_to_topic(self, topic: str, message: dict, retain: bool = False):
        if retain:
            properties = Properties(PacketTypes.PUBLISH)
            properties.MessageExpiryInterval = 150
            self.log.log('publishing persistent message: topic={} message={}', topic, json.dumps(message))
            self.client.publish(topic=topic, payload=json.dumps(message), retain=True, properties=properties)
        else:
            self.log.log('publishing ephemeral message: topic={} message={}', topic, json.dumps(message))
            self.client.publish(topic=topic, payload=json.dumps(message), retain=False)

    def subscribe(self, topic: str, fn):
        self.log.log('subscribing to topic={}', topic)
        self.client.on_message = fn
        self.client.subscribe(topic=topic)

    def block(self):
        self.client.loop_forever()

    def close(self):
        self.log.log('disconnecting from mqtt server ')
        self.client.disconnect()
