#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.config import date_format, emojis
from utilities.print import empty_carriage_line
from utilities.aws import inspector2_list_coverage
from utilities.aws import inspector2_list_findings
from utilities.pec import check_findings_for_public_exploits
from utilities.filter_criteria import get_filter_criteria


"""
Coverage
"""
def get_inspector_coverage(args):
  coverage = {}
  for i, region in enumerate(args.regions):
    print(f'{empty_carriage_line()}{emojis["globe"]} Getting Inspector coverage in {region} ({i+1}/{len(args.regions)})', end='\r')
    regional_coverage = inspector2_list_coverage(region)
    if not regional_coverage: continue
    coverage[region] = {
      'active': 0,
      'inactive': 0
    }
    for instance in regional_coverage:
      if instance['scanStatus']['statusCode'] == 'ACTIVE':
        coverage[region]['active'] += 1
      else:
        coverage[region]['inactive'] += 1
        if args.detailed:
          if 'uncovered_instances' not in coverage[region]:
            coverage[region]['uncovered_instances'] = []
          coverage[region]['uncovered_instances'].append(instance['resourceId'])

    coverage[region]['total'] = coverage[region]['active'] + coverage[region]['inactive']
    coverage[region]['percentage'] = calculate_coverage_percentage(coverage[region]['active'], coverage[region]['inactive'])
  if coverage: print(f'{empty_carriage_line()}{emojis["globe"]} Obtained Inspector coverage ({len(args.regions)}/{len(args.regions)})\n')
  return coverage

def calculate_coverage_percentage(active_instances, inactive_instances):
  try:
    return f'{round(active_instances / (active_instances + inactive_instances) * 100, 2)}%'
  except ZeroDivisionError:
    return '0.0%'


"""
Findings
"""
def get_inspector_findings(args):
  findings = list_inspector_findings(args)
  if findings['all']:
    processed_findings = process_inspector_findings(findings, args)
    return processed_findings
  return None

def list_inspector_findings(args):
  filter_criteria = get_filter_criteria(args)
  findings = {'all': {}}
  for i, region in enumerate(args.regions):
    print(f'{empty_carriage_line()}{emojis["globe"]} Getting findings in {region} ({i+1}/{len(args.regions)})', end='\r')
    regional_findings = inspector2_list_findings(region, filter_criteria)
    if regional_findings:
      findings['all'][region] = regional_findings
  total_findings = sum(len(findings) for findings in findings['all'].values())
  print(f'{empty_carriage_line()}{emojis["globe"]} Obtained {total_findings} finding{"s" if total_findings != 1 else ""}\n')
  return findings

def process_inspector_findings(findings, args):
  if not args.instance_id and not args.cve_id:
    print(f'{empty_carriage_line()}{emojis["factory"]} Processing unique finding{"s" if len(findings) != 1 else ""}', end='\r')
  findings['unique'] = {}
  for region in findings['all']:
    for finding in findings['all'][region]:
      if finding['title'] not in findings['unique']:
        findings['unique'][finding['title']] = {
          'resources': [],
          'severity': finding['severity'],
          'public_exploits': 'n/a'
        }
      findings['unique'][finding['title']]['resources'].append({
        'id': finding['resources'][0]['id'],
        'region': finding['resources'][0]['region'],
        'first_observed': finding['firstObservedAt'].strftime(date_format)
      })
  if not args.instance_id and not args.cve_id:
    print(f'{empty_carriage_line()}{emojis["factory"]} Processed {len(findings["unique"])} unique finding{"s" if len(findings["unique"]) != 1 else ""}\n')
  if not args.skip_public_exploit_check:
    findings = check_findings_for_public_exploits(findings)
  return findings
