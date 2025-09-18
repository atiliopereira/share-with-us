from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

    def __init__(self, *args, **kwargs):
        # Set up session before calling parent init
        self._session = boto3.Session(profile_name='grafiexpress')
        super().__init__(*args, **kwargs)

    @property
    def connection(self):
        if not hasattr(self, '_connection') or self._connection is None:
            self._connection = self._session.resource('s3', region_name=self.region_name)
        return self._connection