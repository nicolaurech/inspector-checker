#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import calendar
from datetime import datetime

from config import config

def parse_arguments():
  parser = argparse.ArgumentParser(formatter_class=ExplicitDefaultsHelpFormatter)
  subparser = parser.add_subparsers(dest='task', required=True)

  # Coverage
  parser_coverage = subparser.add_parser('coverage', formatter_class=ExplicitDefaultsHelpFormatter, help='Check the coverage of Inspector scanning')
  parser_coverage.add_argument('-r', '--region', dest='regions', type=check_region_input, default=config.inspector_supported_regions, help='region to check Inspector')
  parser_coverage.add_argument('-d', '--detailed', action='store_true', help='show uncovered instances')
  parser_coverage.add_argument('-o', '--output', action='store_true', help='save results in a csv file')

  # Findings
  parser_findings = subparser.add_parser('findings', formatter_class=ExplicitDefaultsHelpFormatter, help='Check Inspector findings')

  parser_findings.add_argument('-r', '--region', dest='regions', type=check_region_input, default=config.inspector_supported_regions, help='region to check Inspector')
  parser_findings.add_argument('-s', '--severities', type=check_severities_input, default='critical,high', help=f'comma-separated list of severities. Options: {[s.lower() for s in config.inspector_finding_severities]}')
  parser_findings.add_argument('-t', '--type', dest='finding_type', type=check_finding_type_input, default='package', help=f'type of finding. Options: {[finding_type for finding_type in config.inspector_finding_types]}')
  parser_findings.add_argument('--status', dest='finding_status', type=check_finding_status_input, default='active', help=f'status of findings. Options: {config.inspector_finding_statuses}')
  parser_findings.add_argument('-c', '--cve-id', type=check_cve_id, help='CVE to check')
  parser_findings.add_argument('-i', '--instance-id', type=check_instance_id_input, help='specific instance to check')
  
  # Findings - time
  parser_findings_time_group = parser_findings.add_mutually_exclusive_group()
  parser_findings_time_group.add_argument('--hours', dest='time_hours', type=check_time_hours_days_input, help='Amount of hours before now to check for findings')
  parser_findings_time_group.add_argument('--days', dest='time_days', type=check_time_hours_days_input, help='Amount of days before now to check for findings')
  parser_findings_time_group.add_argument('--month', dest='time_month', type=check_time_month_input, help='Month to check for findings. Without --year option default to current year')
  parser_findings.add_argument('--year', dest='time_year', type=check_time_year_input, help='Year to check for findings. Must have --month specified')
  parser_findings.add_argument('--start-date', dest='time_start_date', type=check_time_date_input, help='Start date to check for findings')
  parser_findings.add_argument('--end-date', dest='time_end_date', type=check_time_date_input, help='End date to check findings')

  parser_findings.add_argument('-d', '--detailed', action='store_true', help='show results by CVE')
  parser_findings.add_argument('--skip-pec', dest='skip_public_exploit_check', action='store_true', help='skip public exploit check')
  parser_findings.add_argument('-o', '--output', action='store_true', help='save the results in a csv file')

  args = parser.parse_args()

  # Custom argument parsing logic
  if args.task == 'findings':
    # Mutually exclusive time
    if args.time_hours or args.time_days or args.time_month:
      if args.time_start_date:
        parser_findings.error('argument --start-date: not allowed with arguments --hours or --months')
      if args.time_end_date:
        parser_findings.error('argument --end-date: not allowed with arguments --hours or --months')
    # Require month when year is specified
    if args.time_year and not args.time_month:
      parser_findings.error('argument --month: must be specified with argument --year')
    # Month and year combination cannot be in the future
    if args.time_month:
      current_year = datetime.now().year
      if not args.time_year: args.time_year = current_year
      # Future year
      if args.time_year > current_year:
        parser_findings.error('argument --year: cannot be in the future')
      months = list(calendar.month_name)
      month_number = months.index(args.time_month.capitalize())
      current_month = datetime.now().month
      # Current year but future month
      if args.time_year == current_year and month_number > current_month:
        parser_findings.error('arguments --month and --year: cannot be in the future')
    
    # Require region when instance id is specified
    if args.instance_id and len(args.regions) != 1:
      parser_findings.error('argument --region: required when instance id is specified')
    
    # Set severities to all allowed when searching by CVE
    if args.cve_id:
      args.severities = config.inspector_finding_severities
    
    # Don't allow detailed when CVE specifed
    if args.detailed and args.cve_id:
      parser_findings.error('argument --detailed: not allowed with argument --cve-id')
    
    # Don't allow detailed when instance id specifed
    if args.detailed and args.instance_id:
      parser_findings.error('argument --detailed: not allowed with argument --instance-id')

  return args

def check_region_input(region):
  if region not in config.inspector_supported_regions:
    raise argparse.ArgumentTypeError(f'unsupported Inspector region: {region}')
  return [region]

def check_time_hours_days_input(time):
  try:
    itime = int(time)
    if itime <= 0:
      raise Exception
    return itime
  except:
    raise argparse.ArgumentTypeError(f'invalid days, must be a positive integer value: {time}')

def check_time_month_input(month):
  try:
    months = calendar.month_name[1:]
    if month.capitalize() not in months:
      raise Exception
    return month
  except:
    raise argparse.ArgumentTypeError(f'invalid month: {month}')

def check_time_year_input(year):
  try:
    year_pattern = '^\d{4}$'
    year_search = re.search(year_pattern, year).group(0)
    return int(year)
  except AttributeError:
    raise argparse.ArgumentTypeError(f'invalid year: {year}')

def check_time_date_input(date):
  try:
    datetime.strptime(date, config.date_format)
    return date
  except ValueError:
    raise argparse.ArgumentTypeError(f'invalid format, should be {config.date_format}')

def check_severities_input(severities):
  severities_list = [s.strip() for s in severities.split(',')]
  for severity in severities_list:
    if severity.upper() not in config.inspector_finding_severities:
      raise argparse.ArgumentTypeError(f'invalid severity: {severity}')
  return severities_list

def check_finding_type_input(finding_type):
  if finding_type not in config.inspector_finding_types:
    raise argparse.ArgumentTypeError(f'invalid finding type: {finding_type}')
  return config.inspector_finding_types[finding_type]

def check_finding_status_input(finding_status):
  if finding_status not in config.inspector_finding_statuses:
    raise argparse.ArgumentTypeError(f'invalid finding status: {finding_status}')
  if finding_status == 'all':
    return [finding_status.upper() for finding_status in config.inspector_finding_statuses if finding_status != 'all']
  return finding_status.upper()

def check_instance_id_input(instance_id):
  try:
    instance_id_pattern = '^i-[\da-f]{12,20}$'
    instance_id_search = re.search(instance_id_pattern, instance_id).group(0)
    return instance_id
  except AttributeError:
    raise argparse.ArgumentTypeError(f'invalid instance id: {instance_id}')

def check_cve_id(cve_id):
  try:
    cve_id_pattern = '^CVE-[\d]{4}-[\d]{1,5}$'
    cve_id_search = re.search(cve_id_pattern, cve_id).group(0)
    return cve_id_search
  except AttributeError:
    raise argparse.ArgumentTypeError(f'invalid CVE id" {cve_id}')

class ExplicitDefaultsHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
  """ Hide default values for options that have None or False default values
  """
  def _get_help_string(self, action):
    if action.default in (None, False):
      return action.help
    return super()._get_help_string(action)
