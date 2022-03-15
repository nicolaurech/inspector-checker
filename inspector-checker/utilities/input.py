#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import calendar
import datetime

from config.config import inspector_supported_regions, allowed_finding_severities, date_format

def parse_arguments():
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  subparser = parser.add_subparsers(dest='task', required=True)

  # Coverage
  parser_coverage = subparser.add_parser('coverage', formatter_class=argparse.ArgumentDefaultsHelpFormatter, help='Check the coverage of Inspector scanning')
  parser_coverage.add_argument('-r', '--region', dest='regions', type=check_region_input, default=inspector_supported_regions, help='region to check Inspector')
  parser_coverage.add_argument('-d', '--detailed', action='store_true', help='show uncovered instances')
  parser_coverage.add_argument('-o', '--output', action='store_true', help='save the results in a csv file')

  # Findings
  parser_findings = subparser.add_parser('findings', formatter_class=argparse.ArgumentDefaultsHelpFormatter, help='Check Inspector findings')

  parser_findings.add_argument('-r', '--region', dest='regions', type=check_region_input, default=inspector_supported_regions, help='region to check Inspector')
  parser_findings.add_argument('-s', '--severities', type=check_severities_input, default='critical,high', help=f'comma-separated list of severities. Options: {[s.lower() for s in allowed_finding_severities]}')
  parser_findings.add_argument('-c', '--cve-id', type=check_cve_id, help='CVE to check')
  parser_findings.add_argument('-i', '--instance-id', type=check_instance_id_input, help='specific instance to check')
  
  # Findings - time
  parser_findings_time_group = parser_findings.add_mutually_exclusive_group()
  parser_findings_time_group.add_argument('--hours', dest='time_hours', type=check_time_hours_days_input, help='something...')
  parser_findings_time_group.add_argument('--days', dest='time_days', type=check_time_hours_days_input, help='something...')
  parser_findings_time_group.add_argument('--month', dest='time_month', type=check_time_month_input, help='something...')
  parser_findings.add_argument('--start-date', dest='time_start_date', type=check_time_date_input, help='something...')
  parser_findings.add_argument('--end-date', dest='time_end_date', type=check_time_date_input, help='something...')

  parser_findings.add_argument('-d', '--detailed', action='store_true', help='show results by CVE')
  parser_findings.add_argument('--skip-pec', dest='skip_public_exploit_check', action='store_true', help='skip public exploit check')
  parser_findings.add_argument('-o', '--output', action='store_true', help='save the results in a csv file')

  args = parser.parse_args()

  if args.task == 'findings':
    # Time
    if args.time_hours or args.time_days or args.time_month:
      if args.time_start_date:
        parser_findings.error('argument --start-date: not allowed with arguments --hours or --months')
      if args.time_end_date:
        parser_findings.error('argument --end-date: not allowed with arguments --hours or --months')
    # Require region when instance id is specified
    if args.instance_id and len(args.regions) != 1:
      parser_findings.error('argument --region: required when instance id is specified')
    # Set severities to all allowed when searching by CVE
    if args.cve_id:
      args.severities = allowed_finding_severities
    # Don't allow detailed when CVE specifed
    if args.detailed and args.cve_id:
      parser_findings.error('argument --detailed: not allowed with argument --cve-id')
    # Don't allow detailed when instance id specifed
    if args.detailed and args.instance_id:
      parser_findings.error('argument --detailed: not allowed with argument --instance-id')

  return args

def check_region_input(region):
  if region not in inspector_supported_regions:
    raise argparse.ArgumentTypeError(f'Unsupported Inspector region: {region}')
  return [region]

def check_time_hours_days_input(time):
  try:
    itime = int(time)
    if itime <= 0:
      raise Exception
    return itime
  except:
    raise argparse.ArgumentTypeError('Value must be a positive integer value')

def check_time_month_input(time):
  try:
    months = calendar.month_name[1:]
    if time.capitalize() not in months:
      raise Exception
    return time
  except:
    raise argparse.ArgumentTypeError('Value must be a valid month')

def check_time_date_input(time):
  try:
    datetime.datetime.strptime(time, date_format)
    return time
  except ValueError:
    raise argparse.ArgumentTypeError(f'Value must be in correct format, should be {date_format}')

def check_severities_input(severities):
  severities_list = [s.strip() for s in severities.split(',')]
  for severity in severities_list:
    if severity.upper() not in allowed_finding_severities:
      raise argparse.ArgumentTypeError(f'Invalid severity: {severity}')
  return severities_list

def check_instance_id_input(instance_id):
  try:
    instance_id_pattern = 'i-[\da-f]{12,20}$'
    instance_id_search = re.search(instance_id_pattern, instance_id).group(0)
    return instance_id
  except:
    raise argparse.ArgumentTypeError('Invalid instance id')

def check_cve_id(cve_id):
  try:
    cve_id_pattern = 'CVE-[\d]{4}-[\d]{1,5}$'
    cve_id_search = re.search(cve_id_pattern, cve_id).group(0)
    return cve_id_search
  except:
    raise argparse.ArgumentTypeError('Invalid CVE id')
