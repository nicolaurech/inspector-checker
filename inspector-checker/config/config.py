#!/usr/bin/env python3
# -*- coding: utf-8 -*-

inspector_checker_version = '1.1'

inspector_supported_regions = [
  'us-east-1',
  'us-east-2',
  'us-west-1',
  'us-west-2',
  'ap-east-1',
  'ap-south-1',
  'ap-northeast-2',
  'ap-southeast-1',
  'ap-southeast-2',
  'ap-northeast-1',
  'ca-central-1',
  'eu-central-1',
  'eu-west-1',
  'eu-west-2',
  'eu-west-3',
  'eu-north-1',
  'sa-east-1'
]

allowed_finding_severities = [
  'CRITICAL',
  'HIGH',
  'MEDIUM',
  'LOW',
  'INFORMATIONAL',
  'UNTRIAGED'
]

date_format = '%m-%d-%Y'

emojis = {
  'chart': '\U0001F4C8',
  'globe': '\N{earth globe europe-africa}',
  'factory': '\N{factory}',
  'magnifying_glass': '\U0001F50D',
  'detective': '\U0001F575',
  'robot': '\U0001F916'
}
