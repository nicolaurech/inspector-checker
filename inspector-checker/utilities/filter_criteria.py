#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import calendar

def get_filter_criteria(args):
  # Default -> active status and severities
  filter_criteria = {
    'findingStatus': [get_filter_criteria_values(comparison='EQUALS', value='ACTIVE')],
    'severity': [get_filter_criteria_values(comparison='EQUALS', value=severity.upper()) for severity in args.severities],
  }
  # Time
  time_filter_criteria = get_time_filter_criteria(args)
  if time_filter_criteria: filter_criteria['firstObservedAt'] = time_filter_criteria
  # Instance ID
  if args.instance_id: filter_criteria['resourceId'] = [get_filter_criteria_values(comparison='EQUALS', value=args.instance_id)]
  # CVE
  if args.cve_id: filter_criteria['title'] = [get_filter_criteria_values(comparison='PREFIX', value=args.cve_id)]
  return filter_criteria

def get_filter_criteria_values(comparison, value):
  return {
    'comparison': comparison,
    'value': value
  }

def get_time_filter_criteria(args):
  time_filter_criteria = []
  
  # Hours
  if args.time_hours:
    now = datetime.now()
    past = now - timedelta(hours = args.time_hours)
    time_filter_criteria = get_first_observed_at_filter_criteria(past, now)

  # Days
  elif args.time_days:
    now = datetime.now()
    past = now - timedelta(days = args.time_days)
    time_filter_criteria = get_first_observed_at_filter_criteria(past, now)

  # Month
  elif args.time_month:
    current_year = datetime.now().year
    months = list(calendar.month_name)
    month_number = months.index(args.time_month.capitalize())
    month_range = calendar.monthrange(current_year, month_number)
    last_day = month_range[1]
    first_of_month = datetime(current_year, month_number, 1)
    last_of_month = datetime(current_year, month_number, last_day, 23, 59, 59, 999999)
    time_filter_criteria = get_first_observed_at_filter_criteria(first_of_month, last_of_month)

  # Start and end date
  elif args.time_start_date and args.time_end_date:
    start_date_items = args.time_start_date.split('-')
    start_month = int(start_date_items[0])
    start_day = int(start_date_items[1])
    start_year = int(start_date_items[2])
    start_date = datetime(start_year, start_month, start_day)

    end_date_items = args.time_end_date.split('-')
    end_month = int(end_date_items[0])
    end_day = int(end_date_items[1])
    end_year = int(end_date_items[2])
    end_date = datetime(end_year, end_month, end_day, 23, 59, 59, 999999)

    time_filter_criteria = get_first_observed_at_filter_criteria(start_date, end_date)

  return time_filter_criteria

def get_first_observed_at_filter_criteria(start, end):
  return [{
    'startInclusive': start,
    'endInclusive': end
  }]
