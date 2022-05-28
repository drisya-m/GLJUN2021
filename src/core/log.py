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

class Log:

    def __init__(self, name: str):
        self.name = name

    def log(self, template: str, *args):
        print('[{}] {}'.format(self.name, template.format(*args)))
