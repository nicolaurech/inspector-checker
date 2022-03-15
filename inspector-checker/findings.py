#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config.config import emojis
from utilities.inspector import get_inspector_findings
from utilities.output import format_findings_data, output_table, output_report, format_detailed_findings_data

def check_inspector_findings(args):
  findings = get_inspector_findings(args)
  if findings:
    data = format_findings_data(findings, args)
    output_table(data, name=f'{emojis["detective"]}  Findings')
    output_report(data, args)
    if args.detailed:
      print(f'{emojis["chart"]} Detailed findings\n')
      detailed_data = format_detailed_findings_data(findings)
      for finding_title in detailed_data:
        output_table(detailed_data[finding_title], name=f'{emojis["pin"]} {finding_title}', style='STYLE_COMPACT')
      if args.output:
        formatted_detailed_report_data = []
        for i, finding_title in enumerate(detailed_data):
          formatted_detailed_report_data.append([finding_title])
          for line in detailed_data[finding_title]:
            formatted_detailed_report_data.append(line)
          if i != len(detailed_data) - 1:
            formatted_detailed_report_data.append([])
        output_report(formatted_detailed_report_data, args, detailed_override=True)
