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
########################################################################################
##
##   888       888        d8888 8888888b.  888b    888 8888888 888b    888  .d8888b.
##   888   o   888       d88888 888   Y88b 8888b   888   888   8888b   888 d88P  Y88b
##   888  d8b  888      d88P888 888    888 88888b  888   888   88888b  888 888    888
##   888 d888b 888     d88P 888 888   d88P 888Y88b 888   888   888Y88b 888 888
##   888d88888b888    d88P  888 8888888P"  888 Y88b888   888   888 Y88b888 888  88888
##   88888P Y88888   d88P   888 888 T88b   888  Y88888   888   888  Y88888 888    888
##   8888P   Y8888  d8888888888 888  T88b  888   Y8888   888   888   Y8888 Y88b  d88P
##   888P     Y888 d88P     888 888   T88b 888    Y888 8888888 888    Y888  "Y8888P88
##
########################################################################################
##
## DO NOT USE THIS CODE IN LAMBDA FUNCTION. THIS IS ONLY FOR DEV TESTING SMALL CODE
##

from jwthelper import JwtHelper


def generate_test_token(identity: str):
    jh = JwtHelper(secret=identity)
    return jh.create_jwt(identity=identity, minutes=10880)


print(generate_test_token('taxi001'))
