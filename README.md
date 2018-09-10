# ActivitiesCacheParser
Parse Windows ActivitiesCache to JSONL or formatted output.

# Usage
```
usage: winactivities2json.py [-h] -s SOURCE [-t TEMP_DIR]
                             [--sequence SEQUENCE] [-o OUTPUT_TEMPLATE]
                             [--dump_db] [--debug {ERROR,WARN,INFO,DEBUG}]

Interface to parse Windows Timeline - ActivitiesCache.db.
Run this tool on the database file, or on a logical volume to process records for all users.

(default location - \Users\%USERNAME%\AppData\Local\ConnectedDevicesPlatform\L.%USERNAME%)

version: 0.0.1

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The activities database or a logical volume (logical
                        volume: \\.\C:).
  -t TEMP_DIR, --temp_dir TEMP_DIR
                        The template directory for extractions if source is a
                        logical volume.
  --sequence SEQUENCE   Only display sequences above this value. (default: 0)
  -o OUTPUT_TEMPLATE, --output_template OUTPUT_TEMPLATE
                        Output template format.
  --dump_db             Dump the entire ActivitiesCache.db database, not just
                        the Activity table.
  --debug {ERROR,WARN,INFO,DEBUG}
                        Debug level [default=ERROR]
```

## Formatted Output
An output template allows you to customize the output instead of the default JSONL format.

By default, no template will cause the tool to output as jsonl format. The template is really just a custom formatted
string.

Given the following record (formatted with indention for better readability):
```json
{
  "_rowid": 115,
  "Id": "c6fbf27c49fb82315155669f8329c995",
  "AppId": [{
      "application": "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe",
      "platform": "windows_win32"
    }, {
      "application": "{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\\WindowsPowerShell\\v1.0\\powershell.exe",
      "platform": "packageId"
    }, {
      "application": "",
      "platform": "alternateId"
    }, {
      "application": "",
      "platform": "windows_universal"
    }
  ],
  "PackageIdHash": "k6rI3Te3bxJRvjak0sx3vVZjSTM2c6pZ22Lb+ebZW6A=",
  "AppActivityId": "ECB32AF3-1440-4086-94E3-5311F97F89C4",
  "ActivityType": 6,
  "ActivityStatus": 1,
  "ParentActivityId": "00000000000000000000000000000000",
  "Tag": null,
  "Group": null,
  "MatchId": null,
  "LastModifiedTime": "2018-07-13 17:03:54",
  "ExpirationTime": "2018-08-12 17:03:54",
  "Payload": {
    "type": "UserEngaged",
    "reportingApp": "ShellActivityMonitor",
    "activeDurationSeconds": 142,
    "shellContentDescription": {
      "MergedGap": 600
    },
    "userTimezone": "America\/Los_Angeles"
  },
  "Priority": 3,
  "IsLocalOnly": 0,
  "PlatformDeviceId": "zdb2vOpgPSkxd2PLwsayEmxe1DNFt6GOtaz+2ENpgLU=",
  "CreatedInCloud": 0,
  "StartTime": "2018-07-13 17:01:36",
  "EndTime": "2018-07-13 17:13:28",
  "LastModifiedOnClient": "2018-07-13 17:13:28",
  "GroupAppActivityId": "",
  "ClipboardPayload": null,
  "EnterpriseId": "",
  "OriginalPayload": null,
  "OriginalLastModifiedOnClient": null,
  "ETag": 687,
  "_user": "mpowers",
  "_cpd_location": "L.mpowers"
}
```

We could pass in a template of `-o "{StartTime} - {AppId[0][application]}"` that would result in the
following output:

```
2018-07-13 17:01:36 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe
```

## Example 1
Using the format template, we want to easily see what activity is recorded for which users having to do with 
cmd.exe. We can grep our data for faster identification.

```
winactivities2json.py -s \\.\H: -t D:\Testing\activities --debug ERROR -o "{_user}: {StartTime} - {AppId[0][application]}" | rg cmd.exe
Administrator: 2018-08-07 19:29:59 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
Administrator: 2018-08-07 19:29:59 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
mpowers: 2018-07-23 13:30:04 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
mpowers: 2018-07-16 17:30:53 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
mpowers: 2018-07-12 21:26:43 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
mpowers: 2018-07-12 21:26:43 - {1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\cmd.exe
```

## TODO Docs
Examples and descriptions of:
- --sequence
- --dump_db