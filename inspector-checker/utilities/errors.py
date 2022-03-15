#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from config.config import emojis
from utilities.print import empty_carriage_line

def endpoint_connection_error(region):
  print(f'{empty_carriage_line()}{emojis["prohibited"]} Unable to connect to Inspector in {region}')

def no_credentials_error():
  print(f'{empty_carriage_line()}{emojis["prohibited"]} Unable to locate AWS credentials')
  sys.exit(1)
