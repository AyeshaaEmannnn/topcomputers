import boto3
import mimetypes
import os
from dotenv import load_dotenv

load_dotenv()  # load .env file

S3_CLIENT = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    endpoint_url=os.getenv("AWS_S3_ENDPOINT_URL")
)

BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

def get_files_with_signed_urls(prefix="products/", expires_in=3600):
    files = []
    continuation_token = None

    while True:
        if continuation_token:
            response = S3_CLIENT.list_objects_v2(
                Bucket=BUCKET_NAME,
                Prefix=prefix,
                ContinuationToken=continuation_token
            )
        else:
            response = S3_CLIENT.list_objects_v2(
                Bucket=BUCKET_NAME,
                Prefix=prefix
            )

        objects = response.get('Contents', [])

        for obj in objects:
            key = obj['Key']
            file_name = key.split("/")[-1]

            url = S3_CLIENT.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': key,
                    'ResponseContentDisposition': f'attachment; filename="{file_name}"'
                },
                ExpiresIn=expires_in
            )

            mime_type, _ = mimetypes.guess_type(key)
            is_image = mime_type and mime_type.startswith("image")
            file_size_mb = round(obj['Size'] / (1024 * 1024), 2)
            name_parts = file_name.rsplit('.', 1)
            title = name_parts[0]
            file_extension = f".{name_parts[1]}" if len(name_parts) > 1 else ""

            files.append({
                "title": title,
                "description": "",
                "file_url": url,
                "is_image": is_image,
                "file_type": mime_type or "unknown",
                "file_size_mb": file_size_mb,
                "file_extension": file_extension,
                "key": key
            })

        # pagination exit check
        if not response.get('IsTruncated'):
            break
        continuation_token = response.get('NextContinuationToken')

    return files
