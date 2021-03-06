import json
import boto3
import os

from datetime import datetime

class Uploader:

    def __init__(self):

        """
            Initializes the AWS SDK / Client and loads the config.json details
        """

        try:
            with open('config.json', 'r') as f:
                config = json.load(f)

                self.serial_no = config['serial_no']
                self.bucket_name = config['bucket_name']

        except:
            print("\n\nWARNING: config.json with serial_no, bucket_name fields must be present\n")
            raise

        self.s3_client = boto3.client('s3')


    def upload_logs(self, path):

        """
            Scans the directory and uploads all contained files to S3 to be processed by CloudWatch.
        """
        if os.path.exists(path):
            filenames = os.listdir(path)
            time_str = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            for filename in filenames:
                print("uploading:", os.path.join(path, filename))

                self.s3_client.upload_file( os.path.join(path, filename), self.bucket_name, f'{self.serial_no}/{time_str}/{filename}')

            print("All Files uploaded")

        else:
            print("No directory specified")


