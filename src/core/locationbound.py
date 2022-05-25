#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Restricted Software.
# Copyright (c) 2021 Palo Alto Networks Inc.
# All Rights Reserved.
#
# @author Anirudh Kushwah
# @since 2022.05
#

class LocationBound:
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float

    def is_valid(self, latitude: float, longitude: float) -> bool:
        if latitude < self.min_latitude or latitude > self.max_latitude:
            return False
        if longitude < self.min_longitude or longitude > self.max_longitude:
            return False
        return True
