#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2022 My Great Learning.
# All Rights Reserved.
#
# @author Anirudh Kushwah
# @since 2022.05
# @Update Drisya - 18.05.2022
import json

import requests
import json

class UserRegistration:
    URL = "https://8wbn03xbll.execute-api.us-east-1.amazonaws.com/v1/register"
    headers = {"Content-Type": "application/json"}
    data = {}

    def user_registration(self, username):
        data = {"username": username}
        print(json.dumps(json.dumps(data)))
        response = requests.request("POST", self.URL, headers=self.headers, data=data)
        print(response.text)


user = UserRegistration()
user.user_registration("drisya")
