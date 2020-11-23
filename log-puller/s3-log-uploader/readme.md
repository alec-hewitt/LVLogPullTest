## Overview

Uploads text logs in specified folder to the appropriate S3 bucket for later processing by CloudWatch.

#### Configuring

- Ask AWS administrator for pi_log_s3_automation credentials.
- Load ~/.aws/credentials file with credentials

Install AWS SDK dependency
```pip install boto3```

Ensure config.json contains appropriate device serial number.
```
{
    "serial_no": "XJ_DEMO_001",
    "bucket_name": "lv-edge-device-logs"
}
```


#### Usage
```
from uploader import Uploader
uploader = Uploader()

# Upload path containing logs
uploader.upload_logs('logs')
```
