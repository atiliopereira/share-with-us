import boto3
from decouple import config

print("USE_S3:", config("USE_S3"))
print("Bucket:", config("AWS_STORAGE_BUCKET_NAME"))

# Add profile parameter
session = boto3.Session(profile_name="grafiexpress")
s3 = session.client("s3", region_name=config("AWS_S3_REGION_NAME"))

print("S3 connection successful")
print("Buckets:", [b["Name"] for b in s3.list_buckets()["Buckets"]])
