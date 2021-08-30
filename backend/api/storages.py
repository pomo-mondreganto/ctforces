import os
from storages.backends.s3boto3 import S3Boto3Storage


class BaseStorage(S3Boto3Storage):
    def path(self, name):
        return self.url(name)

    def get_accessed_time(self, name):
        return None

    def get_created_time(self, name):
        return None


class DefaultStorage(BaseStorage):
    bucket_name = os.getenv('S3_BUCKET', 'ctforces')
    bucket_acl = 'private'
