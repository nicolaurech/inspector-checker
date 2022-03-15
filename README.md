# inspector-checker

AWS Inspector is an automated vulnerability management service that continually scans AWS workloads for software vulnerabilities and unintended network exposure.

`inspector-checker` is a programmatic companion to the AWS Inspector service. It tries to make up for some of the inherent weaknesses of the Inspector dashboard by making it quick and easy to check and visualize findings across an AWS environment.

# Setup

```
git clone git@github.com:nicolaurech/inspector-checker.git
cd inspector-checker

pip install -r requirements.txt

ln -s $(pwd)/inspector-checker/inspector-checker.py /usr/local/bin/inspector-checker
```

# Usage

`inspector-checker` can perform two main functions:
- Check coverage
- Check findings

## Coverage
The check coverage function provides insight into how instances are covered (i.e. being scanned). It can also highlight the instances that are not covered.

By default, it shows:
- Active instances
- Inactive instances
- Total instances
- The percentage of instances covered

### Options
- Region
- Detailed
- Output

Help:
```
inspector-checker coverage -h
```

Check coverage in all regions:
```
inspector-checker coverage
```

Check coverage in a specific region:
```
inspector-checker coverage -r us-east-1
```

Check the uncovered instances in all regions:
```
inspector-checker coverage -d
```

Check the uncovered instances in a specific region:
```
inspector-checker coverage -r us-east-1 -d
```

Save the output in a csv file:
```
inspector-checker coverage -o
inspector-checker coverage -r us-east-1 -d -o
```

## Findings
The check findings function provides insight into the Inspector findings across an AWS environment. It can highlight all findings, only show recent findings, search for findings with a specified severity, search for CVEs, check specified instances, etc.

By default, it shows:
- All active CVEs across the AWS environment
- The frequency of each CVE across the AWS environment
- Public exploits associated with CVEs (via Sploitus)
- The severity of each CVE

Additionally, it can show:
- The most recent findings across an AWS environment
- Findings in a specified month
- Findings in a specified time range
- Findings with given severities
- If a specified CVE has been found in the AWS environment
- What findings a given EC2 instance has

### Options
- Region
- Severities
- CVE
- Instance
- Hours
- Days
- Month
- Start date
- End date
- Detailed
- Skip public exploit check
- Save output

Help:
```
inspector-checker findings -h
```

Check active findings in all regions:
```
inspector-checker findings
```

Check active findings in a specified region:
```
inspector-checker findings -r us-east-1
```

Check recent findings:
```
inspector-checker findings --hours 24
inspector-checker findings --days 7
inspector-checker findings --days 30
```

Check findings in a specified month this year:
```
inspector-checker findings --month february
inspector-checker findings --month march -r us-east-1
```

Check findings in a specified time range:
```
inspector-checker findings --start-date 3-5-2022 --end-date 3-16-2022
inspector-checker findings --start-date 2-1-2022 --end-date 2-2-2022
```

Check findings with specified severities (default is critical and high):
```
inspector-checker findings -s medium
inspector-checker findings -s high,medium
inspector-checker findings -s informational
inspector-checker findings --month february -s critical
inspector-checker findings --days 7 -s critical
```

Check the findings for a specified instance in a region:
```
inspector-checker findings -i i-0aa55b666c7dd8e99 -r us-east-1
inspector-checker findings -i i-0aa55b666c7dd8e99 -r us-east-1 --hours 24
inspector-checker findings -i i-0aa55b666c7dd8e99 -r us-east-1 --days 14
```

Check if a CVE has been found in the AWS environment:
```
inspector-checker findings -c CVE-2010-1122
inspector-checker findings -c CVE-2010-1122 -r us-east-1
inspector-checker findings -c CVE-2010-1122 -r us-east-1 --days 5
inspector-checker findings -c CVE-2010-1122 -r us-east-1 --hours 12
inspector-checker findings -c CVE-2010-1122 -r us-east-1 -i i-0aa55b666c7dd8e99
```

Skip public exploit check (enabled by default):
```
inspector-checker findings --skip-pec
```

Get detailed output:
```
inspector-checker findings -d
inspector-checker findings --hours 24 -d
inspector-checker findings --start-date 3-5-22 --end-date 3-16-22 -d
```

Save the output to a csv file:
```
inspector-checker findings -o
inspector-checker findings -d -o
inspector-checker findings --days 7 -o
inspector-checker findings -c CVE-2010-1122 -r us-east-1 -o
inspector-checker findings -i i-0aa55b666c7dd8e99 -r us-east-1 -o
```

# Future Improvements
- Add other report formats (e.g. json)
- Add support for container scanning and findings
- Allow searching of non-CVE findings (e.g. "port range")
- Add colors to highlight (more) important information
- Add support for suppressed, closed and all findings
- Improve (internal) documentation
- Add support for past years when specifying month
- Tests
