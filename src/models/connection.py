import json
from s3 import S3Processor


class Connection:
    def __init__(self, credentials_file: str):
        self.s3_credentials = None

        with open(credentials_file, 'r') as file:
            self.s3_credentials = json.load(file)

        self.s3_processor = S3Processor(akid=self.s3_credentials['AKID'], sak=self.s3_credentials['SAK'], region=self.s3_credentials['Region'])

    def get_records_list(self) -> list:
        return self.s3_processor.list(selected_bucket=self.s3_credentials['S3 bucket name'], json=True)
 
    def get_record(self, object_key) -> dict:
        data = self.s3_processor.get(selected_bucket=self.s3_credentials['S3 bucket name'], object_key=object_key)
        data = json.loads(data)

        return data
    