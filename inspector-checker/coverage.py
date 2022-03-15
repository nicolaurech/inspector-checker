#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.config import emojis
from utilities.inspector import get_inspector_coverage
from utilities.output import format_coverage_data, output_table, output_report, format_detailed_coverage_data

def check_inspector_coverage(args):
  coverage = get_inspector_coverage(args)
  if coverage:
    data = format_coverage_data(coverage)
    output_table(data, name=f'{emojis["robot"]} Coverage')
    output_report(data, args)
    if args.detailed:
      print(f'{emojis["chart"]} Detailed coverage\n')
      for region in coverage:
        detailed_data = format_detailed_coverage_data(coverage[region]['uncovered_instances'])
        output_table(detailed_data, name=f'{emojis["map"]}  {region}', style='STYLE_COMPACT')
        if args.output:
          output_report(detailed_data, args, region_override=region)
