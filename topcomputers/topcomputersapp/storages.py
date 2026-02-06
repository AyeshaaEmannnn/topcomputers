from storages.backends.s3boto3 import S3Boto3Storage

class ProductStorage(S3Boto3Storage):
    bucket_name = 'topcomputers'    # aapka bucket name
    location = 'products'            # ye folder ka naam hai
    default_acl = 'public-read'      # files public hongi
