#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import EndpointConnectionError, NoCredentialsError

from utilities.errors import endpoint_connection_error, no_credentials_error

def inspector2_list_findings(region, filter_criteria):
  try:
    regional_findings = []
    inspector2_client = boto3.client('inspector2', region_name=region)
    response = inspector2_client.list_findings(filterCriteria=filter_criteria)
    regional_findings.extend(response['findings'])
    while 'nextToken' in response:
      response = inspector2_client.list_findings(
        filterCriteria=filter_criteria,
        nextToken=response['nextToken']
      )
      regional_findings.extend(response['findings'])
  except EndpointConnectionError:
    endpoint_connection_error(region)
  except NoCredentialsError:
    no_credentials_error()
  return regional_findings

def inspector2_list_coverage(region):
  try:
    coverage = []
    inspector2_client = boto3.client('inspector2', region_name=region)
    coverage = inspector2_client.list_coverage(
      filterCriteria={
        'resourceType': [
          {
            'comparison': 'EQUALS',
            'value': 'AWS_EC2_INSTANCE'
          }
        ]
      }
    )['coveredResources']
  except EndpointConnectionError:
    endpoint_connection_error(region)
  except NoCredentialsError:
    no_credentials_error()
  return coverage
