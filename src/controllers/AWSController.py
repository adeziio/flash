from boto3 import resource
from src.configs import AWSConfig

AWS_ACCESS_KEY_ID = AWSConfig.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWSConfig.AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME = AWSConfig.AWS_REGION_NAME

resource = resource(
    'dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)
KarmaController = resource.Table("yoshii-karma")
