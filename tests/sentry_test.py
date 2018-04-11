#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author:fsh
#time:'2018/4/7 14:09:35下午'
from raven import Client

client = Client('https://ffd8de5950894e16aef7f1e358e761e1:265240370fbe4e11a78c57edc4030c4c@sentry.io/1146563')

try:
    1 / 0
except ZeroDivisionError:
    client.captureException()