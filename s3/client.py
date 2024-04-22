import logging

import urllib3
from minio import Minio
from minio.error import S3Error


class S3Browser:
    def __init__(self, data: dict, proxy: dict|None) -> None:
        # Data values
        self.address = data['address']
        self.access_key = data['accessKey']
        self.secret_key = data['secretKey']
        self.bucket = data['bucket']
        self.secure = data['use_ssl']
        # Proxy
        self.use_proxy = proxy['enabled']
        self.proxy_address = proxy['address']
        self.proxy_port = proxy['port']
        # Client
        self.client = self.connect()

    def connect(self) -> None:
        logging.info(f"Server '{self.address}', access key '{self.access_key}'")
        if self.use_proxy is False:
            client = Minio(
                endpoint=self.address,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=False if self.secure is False else True,
            )
        else:
            client = Minio(
                endpoint=self.address,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=False if self.secure is False else True,
                http_client=urllib3.ProxyManager(
                    f"http://{self.proxy_address}:{self.proxy_port}/",
                    timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                    cert_reqs="CERT_REQUIRED",
                    retries=urllib3.Retry(
                        total=5,
                        backoff_factor=0.2,
                        status_forcelist=[500, 502, 503, 504],
                    ),
                ),
            )

        return client

    def make_bucket(self) -> None:
        """ Create a bucket. """
        client = self.client

        logging.info(f"Creating bucket '{self.bucket}'")
        try:
            client.make_bucket(self.bucket)
        except S3Error as exc:
            logging.error(f"Failed to create bucket. Exception: {exc}")
            exit(1)

    def list_buckets(self) -> None:
        """ List information of all accessible buckets. """
        client = self.client

        logging.info("Listing all buckets...")
        try:
            buckets = client.list_buckets()
        except S3Error as exc:
            logging.error(f"Failed to list buckets. Exception: {exc}")
            exit(1)

        logging.info(f"Found buckets: {len(buckets)}")
        for bucket in buckets:
            logging.info(f"Bucket name: {bucket.name}, Creation date: {bucket.creation_date}")

    def bucket_exists(self) -> bool:
        """ Checks if a bucket exists. """
        client = self.client

        logging.info(f"Checking if bucket '{self.bucket}' exists")
        try:
            if client.bucket_exists(self.bucket):
                exists = True
            else:
                exists = False
        except S3Error as exc:
            logging.error(f"Failed to check if bucket exists. Exception: {exc}")
            exit(1)

        logging.info(f"Bucket '{self.bucket}' exists: {exists}")
        return exists

    def list_objects(self) -> None:
        """ Lists object information of a bucket. """
        client = self.client

        logging.info(f"Getting objects from bucket '{self.bucket}'")
        try:
            objects = client.list_objects(self.bucket)
        except S3Error as exc:
            logging.error(f"Failed to list objects. Exception: {exc}")
            exit(1)

        for obj in objects:
            logging.info(f"Object name: {obj.object_name}, Last Modified: {obj.last_modified}, Size: {obj.size}")

    def get_object(self, object_name) -> None:
        """ Gets data from offset to length of an object. """
        client = self.client

        logging.info(f"Getting file '{object_name}' from bucket '{self.bucket}'")
        try:
            data = client.get_object(self.bucket, object_name)
        except S3Error as exc:
            logging.error(f"Failed to get object. Exception: {exc}")
            exit(1)

        for obj in data:
            logging.info(f'Object name: {obj.object_name}, Last Modified: {obj.last_modified}, Size: {obj.size}')

    def fput_object(self, object_name, data) -> None:
        """ Uploads data from a file to an object in a bucket. """
        client = self.client

        logging.info(f"Uploading file '{object_name}' to bucket '{self.bucket}'")

        try:
            # if self.bucket_exists() is False:
            #     logging.error(f"Bucket '{self.bucket}' does not exist")
            #     exit(1)

            client.fput_object(self.bucket, object_name, data)
        except S3Error as exc:
            logging.error(f"Failed to upload object. Exception: {exc}")
            exit(1)

        logging.info(f"Uploaded file '{object_name}' to bucket '{self.bucket}'")

    def remove_object(self, object_name) -> None:
        """ Remove an object. """
        client = self.client

        logging.info(f"Deleting file '{object_name}' from bucket '{self.bucket}'")

        try:
            client.remove_object(self.bucket, object_name)
        except S3Error as exc:
            logging.error(f"Failed to delete object. Exception: {exc}")
            exit(1)

        logging.info(f"Deleted file '{object_name}' from bucket '{self.bucket}'")

    def fget_object(self, object_name, object_path) -> None:
        """ Downloads data of an object to file. """
        client = self.client

        logging.info(f"Downloading file '{object_name}' from bucket '{self.bucket}'")

        try:
            client.fget_object(self.bucket, object_name, object_path)
        except S3Error as exc:
            logging.error(f"Failed to download object. Exception: {exc}")
            exit(1)

        logging.info(f"Downloaded file '{object_name}' from bucket '{self.bucket}' to '{object_path}'")

    def stat_object(self, object_name) -> None:
        """ Get object information and metadata of an object. """
        client = self.client

        logging.info(f"Stating file '{object_name}' in bucket '{self.bucket}'")
        try:
            data = client.stat_object(self.bucket, object_name)
        except S3Error as exc:
            logging.error(f"Failed to get object. Exception: {exc}")
            exit(1)

        logging.info(f"Stated object name: {data.object_name}, Last Modified: {data.last_modified}, Size: {data.size}")

    def get_bucket_policy(self) -> None:
        """ Get bucket policy. """
        client = self.client

        logging.info(f"Getting bucket policy from bucket '{self.bucket}'")
        try:
            policy = client.get_bucket_policy(self.bucket)
        except S3Error as exc:
            logging.error(f"Failed to get bucket policy. Exception: {exc}")
            exit(1)

        logging.info(f"Bucket policy: {policy}")
