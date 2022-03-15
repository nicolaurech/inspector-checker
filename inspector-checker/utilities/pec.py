#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import json

from config.config import emojis
from utilities.print import empty_carriage_line

def check_findings_for_public_exploits(findings):
  request_parameters = {
    'url': 'https://sploitus.com/search',
    'headers': {'content-type': 'application/json'},
    'payload': {
      'type': 'exploits',
      'sort': 'default',
      'title': False,
      'offset': 0
    }
  }
  for i, finding_title in enumerate(findings['unique']):
    findings['unique'][finding_title]['public_exploits'] = check_finding_for_public_exploits(request_parameters, finding_title, finding_number=i+1, number_of_findings=len(findings["unique"]))
  print(f'{empty_carriage_line()}{emojis["magnifying_glass"]} Checked {len(findings["unique"])} CVE{"s" if len(findings["unique"]) != 1 else ""} for public exploits\n')
  return findings

def check_finding_for_public_exploits(request_parameters, finding, finding_number, number_of_findings):
  try:
    cve_pattern = 'CVE-\d{4}-\d{1,5}'
    cve_id = re.search(cve_pattern, finding).group(0)
    request_parameters['payload']['query'] = cve_id
    print(f'{empty_carriage_line()}{emojis["magnifying_glass"]} Checking {cve_id} for public exploits ({finding_number}/{number_of_findings})', end='\r')
    response = requests.post(url=request_parameters['url'], data=json.dumps(request_parameters['payload']), headers=request_parameters['headers']).text
    number_of_exploits = json.loads(response)['exploits_total']
    return number_of_exploits
  except (AttributeError, json.decoder.JSONDecodeError):
    return 'n/a'
