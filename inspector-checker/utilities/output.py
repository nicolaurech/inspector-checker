#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
from datetime import datetime
from beautifultable import BeautifulTable

from config.config import date_format


"""
General
"""
def get_project_path():
  return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_output_path():
  return f'{get_project_path()}/output'

def create_output_directory(output_path):
  if not os.path.isdir(output_path):
    os.mkdir(output_path)

def get_report_path(output_path, args, region_override, detailed_override):
  return f'{output_path}/{get_report_name(args, region_override, detailed_override)}'

def get_report_name(args, region_override, detailed_override):
  report_name = f'ic-{args.task}'
  # Add region
  if type(args.regions) == str or len(args.regions) == 1:
    report_name += f'-{"".join(args.regions)}'
  if region_override:
    report_name += f'-{region_override}'
  # Add month
  if args.task == 'findings' and args.time_month:
    report_name += f'-{args.time_month}'
  # Add detailed
  if args.detailed and detailed_override:
    report_name += f'-detailed'
  # Add instance id
  if args.task == 'findings' and args.instance_id:
    report_name += f'-{args.instance_id}'
  # Add CVE
  if args.task == 'findings' and args.cve_id:
    report_name += f'-{args.cve_id}'
  # Add date
  report_name += f'-{datetime.now().strftime(date_format)}.csv'
  return report_name

def output_report(data, args, region_override=None, detailed_override=None):
  if not args.output: return
  output_path = get_output_path()
  create_output_directory(output_path)
  report_path = get_report_path(output_path, args, region_override, detailed_override)
  with open(report_path, 'w') as report_file:
    csv_writer = csv.writer(report_file, delimiter=',')
    for line in data:
      csv_writer.writerow(line)

def output_table(data, name, style='STYLE_BOX_DOUBLED'):
  print(f'{name}\n')
  # Populate
  table = BeautifulTable(maxwidth=os.get_terminal_size().columns)
  table.columns.header = data[0]
  for row in data[1:]:
    table.rows.append(row)
  # Alignment
  table.columns.alignment = BeautifulTable.ALIGN_LEFT
  # Style
  table.set_style(getattr(BeautifulTable, style))
  print(f'{table}\n')


"""
Coverage
"""
def format_coverage_data(coverage):
  headers = [
    'Region',
    'Active Instances',
    'Inactive Instances',
    'Total Instances',
    'Coverage'
  ]
  data = [headers]
  for region in coverage:
    data.append([
      region,
      coverage[region]['active'],
      coverage[region]['inactive'],
      coverage[region]['total'],
      coverage[region]['percentage']
    ])
  return data

def format_detailed_coverage_data(instances):
  headers = [
    'Uncovered Instances'
  ]
  data =  [headers]
  for instance in instances:
    data.append([
      instance
    ])
  return data


"""
Findings
"""
def format_findings_data(findings, args):
  # Default -> summary
  if not args.instance_id and not args.cve_id:
    headers = [
      'Finding',
      'Severity',
      'Occurrences',
      'Public Exploits'
    ]
    data = [headers]
    for finding_title in findings['unique']:
      data.append([
        finding_title,
        findings['unique'][finding_title]['severity'],
        len(findings['unique'][finding_title]['resources']),
        findings['unique'][finding_title]['public_exploits']
      ])
  # Instance specified
  elif args.instance_id and not args.cve_id:
    headers = [
      'Finding',
      'Severity',
      'Public Exploits',
      'First Observed'
    ]
    data = [headers]
    for finding_title in findings['unique']:
      for resource in findings['unique'][finding_title]['resources']:
        data.append([
          finding_title,
          findings['unique'][finding_title]['severity'],
          findings['unique'][finding_title]['public_exploits'],
          resource['first_observed']
        ])

  # CVE specified
  elif args.cve_id:
    headers = [
      'Finding',
      'Severity',
      'Public Exploits',
      'Resource',
      'Region',
      'First Observed'
    ]
    data = [headers]
    for finding_title in findings['unique']:
      for resource in findings['unique'][finding_title]['resources']:
        data.append([
          finding_title,
          findings['unique'][finding_title]['severity'],
          findings['unique'][finding_title]['public_exploits'],
          resource['id'],
          resource['region'],
          resource['first_observed']
        ])
  return data

def format_detailed_findings_data(findings):
  data = {}
  headers = [
    'Instance',
    'Region'
  ]
  for finding_title in findings['unique']:
    data[finding_title] = [headers]
    for resource in findings['unique'][finding_title]['resources']:
      data[finding_title].append([
        resource['id'],
        resource['region']
      ])
  return data
